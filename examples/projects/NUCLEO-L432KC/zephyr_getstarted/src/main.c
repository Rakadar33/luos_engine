/******************************************************************************
 * @file Test Zephyr with Luos
 * @brief the first test
 * @MCU Family ESP32
 * @author Luos
 * @version 0.0.0
 ******************************************************************************/
#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <string.h>
#include "main.h"
#include "gpio_l4xx.h"
#include "luos_engine.h"
#include "button.h"
#include "robus_hal.h"

/*---------------------------------------------------------------------
 *    Configuration : (for DEBUG)
 *       - BLINK_THREAD : 2 threads => First Thread to blink the LED
 *                                  => Second Thread to stop blinking
 *       - GO_LUOS :  To add Luos
 *---------------------------------------------------------------------*/
#define BLINK_THREAD // uncomment to add 2 blinking threads
// #define GO_LUOS  // uncomment to use Luos

/*---------------------------------------------------------------------
 *    Definitions
 *---------------------------------------------------------------------*/
// size of stack area used by each thread
#define LUOS_STACKSIZE 2048
#define APP_STACKSIZE  512

// scheduling priority used by each thread (1 = minimum priority, 2 = higher priority than 1, ...)
#define LUOS_APP_TASK_PRIORITY 5
#define APP_TASK_PRIORITY      4

// timings definitions (in ms)
#define SLEEP_TIME_MS   1000
#define LED_PERIOD      500
#define LED_STOP_PERIOD 2000

// led definitions
#define LED0_NODE DT_ALIAS(led0) // the devicetree node identifier for the "led0" alias.
#if DT_NODE_HAS_STATUS(LED0_NODE, okay)
    #define LED0  DT_GPIO_LABEL(LED0_NODE, gpios)
    #define PIN   DT_GPIO_PIN(LED0_NODE, gpios)
    #define FLAGS DT_GPIO_FLAGS(LED0_NODE, gpios)
#else
    // A build error here means your board isn't set up to blink an LED.
    #error "Unsupported board: led0 devicetree alias is not defined"
    #define LED0  ""
    #define PIN   0
    #define FLAGS 0
#endif

// variables
static bool thread_run    = false;
static struct device *dev = NULL;
static bool led_state     = true;
static bool led_toggle    = true;

// functions
void isr_config(void);
bool led_config(void);
void THREAD_init(void);
void THREAD_change_led_state(void);
void THREAD_lock_led(void);

// ------------------------------------------------------------------------------------
// START THE THREADS HERE
// ------------------------------------------------------------------------------------
K_THREAD_DEFINE(init_id, LUOS_STACKSIZE, THREAD_init, NULL, NULL, NULL, LUOS_APP_TASK_PRIORITY, 0, 0);
K_THREAD_DEFINE(THREAD_change_led_state_id, APP_STACKSIZE, THREAD_change_led_state, NULL, NULL, NULL, APP_TASK_PRIORITY, 0, 0);
K_THREAD_DEFINE(THREAD_lock_led_id, APP_STACKSIZE, THREAD_lock_led, NULL, NULL, NULL, APP_TASK_PRIORITY, 0, 0);

/*************************************************************************************
 * @brief Luos Thread with highest priority : Confiuration (luos + led) and Luos Loop
 * @param : None
 * @return None
 *************************************************************************************/
void THREAD_init(void)
{
#ifdef GO_LUOS
    isr_config(); // Very ugly : connect IT callbacks
    Luos_Init();
    Button_Init();
#endif

#ifdef BLINK_THREAD
    if (led_config())
    {
        thread_run = true;
    }
#endif

    while (thread_run)
    {
#ifdef GO_LUOS
        Luos_Loop();
        Button_Loop();
#endif
#ifdef BLINK_THREAD
        k_msleep(1);
        //k_yield();
#endif
    }
}

/******************************************************************************
 * @brief Blink Led every LED_PERIOD seconds
 * @param : None
 * @return None
 ******************************************************************************/
void THREAD_change_led_state(void)
{
#ifdef BLINK_THREAD
    thread_run = false;
#endif

    k_msleep(2000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        if (led_toggle)
        {
            gpio_pin_set(dev, PIN, (int)led_state);
            led_state = !led_state;
        }
        //k_yield();
        k_msleep(LED_PERIOD);
    }
}

/******************************************************************************
 * @brief Stop led blinking every LED_STOP_PERIOD seconds
 * @param : None
 * @return None
 ******************************************************************************/
void THREAD_lock_led(void)
{
#ifdef BLINK_THREAD
    thread_run = false;
#endif

    k_msleep(2000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        led_toggle = !led_toggle;
        //k_yield();
        k_msleep(LED_STOP_PERIOD);
    }
}

/******************************************************************************
 * @brief Luos config ISR
 * @param : None
 * @return None
 ******************************************************************************/
void isr_config(void)
{
    HAL_NVIC_DisableIRQ(LUOS_TIMER_IRQ);
    HAL_NVIC_DisableIRQ(LUOS_COM_IRQ);
    HAL_NVIC_DisableIRQ(PTPA_IRQ);
    HAL_NVIC_DisableIRQ(PTPB_IRQ);

    NVIC_ClearPendingIRQ(LUOS_TIMER_IRQ);
    NVIC_ClearPendingIRQ(LUOS_COM_IRQ);
    NVIC_ClearPendingIRQ(PTPA_IRQ);
    NVIC_ClearPendingIRQ(PTPB_IRQ);

    // Connect Luos ITs to zephyr kernel
    irq_connect_dynamic(LUOS_COM_IRQ, 1, (void *)LUOS_COM_IRQHANDLER(), 0, 0);
    irq_connect_dynamic(LUOS_TIMER_IRQ, 2, (void *)LUOS_TIMER_IRQHANDLER(), 0, 0);
    irq_connect_dynamic(PTPA_IRQ, 16, (void *)&HAL_GPIO_EXTI_Callback, PTPA_IRQ, 0);
    irq_connect_dynamic(PTPB_IRQ, 16, (void *)&HAL_GPIO_EXTI_Callback, PTPB_IRQ, 0);

    // Enable ITs
    irq_enable(LUOS_COM_IRQ);
    irq_enable(PTPA_IRQ);
    irq_enable(PTPB_IRQ);
    // *****************************************
    // irq_enable(LUOS_TIMER_IRQ); // uncomment this line, and it's the end of the world : FATAL ASSERT
    // *****************************************
    //  If "irq_enable(LUOS_TIMER_IRQ)" is not commented: crash in _isr_wrapper:
    //      ldr r1, =_sw_isr_table
    //      add r1, r1, r0
    //      ldm r1!,{r0,r3}	/* arg in r0, ISR in r3 */
    //      blx r3		    /* call ISR */   <------ CRASH!!!!!!!!!!!!
    // Register r3 is not loaded with the handler for LUOS_TIMER_IRQ
}

/******************************************************************************
 * @brief Config Led
 * @param : None
 * @return : configuration state (True if OK)
 ******************************************************************************/
bool led_config(void)
{
    int ret;
    // To test 2 others thread to blink a LED
    dev = device_get_binding(LED0);

    if (dev == NULL)
    {
        return false;
    }

    ret = gpio_pin_configure(dev, PIN, GPIO_OUTPUT_ACTIVE | FLAGS);
    if (ret < 0)
    {
        return false;
    }

    return true;
}
