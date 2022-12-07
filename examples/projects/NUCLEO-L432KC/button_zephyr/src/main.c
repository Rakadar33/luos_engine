/**/ //----- Proj mix avec init ok  ----------------------------------------------------------------------------------------------------------
#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <string.h>
#include "main.h"
#include "gpio_l4xx.h"
#include "luos_engine.h"
#include "button.h"

// 1000 msec = 1 sec
#define SLEEP_TIME_MS 1000

// The devicetree node identifier for the "led0" alias.
#define LED0_NODE DT_ALIAS(led0)

// size of stack area used by each thread
#define INIT_STACKSIZE 2048
#define LUOS_STACKSIZE 2048
#define TASK_STACKSIZE 512

// scheduling priority used by each thread
#define TASK_PRIORITY_INIT 9
#define LUOS_PRIORITY_INIT 8
#define TASK_PRIORITY      8

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

static bool thread_run    = false;
static struct device *dev = NULL;
static bool led_state     = true;
static bool led_toggle    = true;

void test_isr(void);
void isr_config(void);
//extern void PINOUT_IRQHANDLER(uint16_t GPIO_Pin);

//D:\_Luos_\2_Code\_Luos_Lib\luos_engine\network\robus\HAL\STM32L4
//#include "robus_hal_config.h"
#include "robus_hal.h"

//-------------------------------   TEST IT DYN -----------------------------
void test_isr(void)
{
    ;
}

//Declare the interrupt handler function
/*
static void ptp_handler(int irq, void *gpio)
{
    HAL_GPIO_EXTI_Callback((uint16_t *)gpio);
}
*/
static void ptp_handler(int32_t irq)
{
    if (irq == PTPA_IRQ)
    {
        HAL_GPIO_EXTI_Callback(PTPA_PIN);
    }
    else if (irq == PTPB_IRQ)
    {
        HAL_GPIO_EXTI_Callback(PTPB_PIN);
    }
}

void isr_config(void)
{

    // HAL_NVIC_SetPriority(LUOS_COM_IRQ,       0   , 1);
    // HAL_NVIC_SetPriority(LUOS_TIMER_IRQ,     0,    2);
    // HAL_NVIC_SetPriority(PTP[i].IRQ,         1,    0);

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
    //irq_disable(LUOS_COM_IRQ);

    irq_connect_dynamic(LUOS_TIMER_IRQ, 2, (void *)LUOS_TIMER_IRQHANDLER(), 0, 0);
    //irq_disable(LUOS_TIMER_IRQ);

    irq_connect_dynamic(PTPA_IRQ, 16, (void *)&HAL_GPIO_EXTI_Callback, PTPA_IRQ, 0);
    irq_connect_dynamic(PTPB_IRQ, 16, (void *)&HAL_GPIO_EXTI_Callback, PTPB_IRQ, 0);

    //irq_connect_dynamic(PTPA_IRQ, 16, (void *)ptp_handler, 0, 0);
    //irq_disable(PTPA_IRQ);

    //irq_connect_dynamic(PTPB_IRQ, 16, (void *)ptp_handler, 0, 0);
    //irq_disable(PTPB_IRQ);

    // Enable ITs
    irq_enable(LUOS_COM_IRQ);
    irq_enable(PTPA_IRQ);
    irq_enable(PTPB_IRQ);
    //irq_enable(LUOS_TIMER_IRQ);
}
//-------------------------------  FIN TEST IT DYN -----------------------------

void init(void)
{
    int ret;
    isr_config();
    Luos_Init();
    Button_Init();
    //isr_config();

    /*
    dev = device_get_binding(LED0);

    if (dev == NULL)
    {
        return;
    }

    ret = gpio_pin_configure(dev, PIN, GPIO_OUTPUT_ACTIVE | FLAGS);
    if (ret < 0)
    {
        return;
    }
    thread_run = true;
*/

    while (1)
    {
        Luos_Loop();
        Button_Loop();
        //k_msleep(1);
        //k_yield();
    }
}

void change_led_state(void)
{
    k_msleep(1000);
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
        k_yield();
        k_msleep(1000);
    }
}

void lock_led(void)
{
    k_msleep(1000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        led_toggle = !led_toggle;
        k_yield();
        k_msleep(6000);
    }
}

K_THREAD_DEFINE(init_id, INIT_STACKSIZE, init, NULL, NULL, NULL, TASK_PRIORITY_INIT, 0, 0);
//K_THREAD_DEFINE(change_led_state_id, TASK_STACKSIZE, change_led_state, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);
//K_THREAD_DEFINE(lock_led_id, TASK_STACKSIZE, lock_led, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);

/**/

/* //----- Proj mix avec init ok  ----------------------------------------------------------------------------------------------------------
#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <string.h>
#include "main.h"
#include "gpio_l4xx.h"
#include "luos_engine.h"
#include "button.h"

// 1000 msec = 1 sec
#define SLEEP_TIME_MS 1000

// The devicetree node identifier for the "led0" alias.
#define LED0_NODE DT_ALIAS(led0)

// size of stack area used by each thread
#define INIT_STACKSIZE 2048
#define LUOS_STACKSIZE 2048
#define TASK_STACKSIZE 512

// scheduling priority used by each thread
#define TASK_PRIORITY_INIT 9
#define LUOS_PRIORITY_INIT 8
#define TASK_PRIORITY      8

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

static bool thread_run
    = false;
static struct device *dev = NULL;
static bool led_state     = true;
static bool led_toggle    = true;

void init(void)
{
    int ret;

    Luos_Init();
    Button_Init();

    dev = device_get_binding(LED0);

    if (dev == NULL)
    {
        return;
    }

    ret = gpio_pin_configure(dev, PIN, GPIO_OUTPUT_ACTIVE | FLAGS);
    if (ret < 0)
    {
        return;
    }
    thread_run = true;
}

void luos(void)
{
    k_msleep(5000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        Luos_Loop();
        Button_Loop();
        k_msleep(1);
        k_yield();
    }
}

void change_led_state(void)
{
    k_msleep(1000);
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
        k_yield();
        k_msleep(1000);
    }
}

void lock_led(void)
{
    k_msleep(1000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        led_toggle = !led_toggle;
        k_yield();
        k_msleep(6000);
    }
}

K_THREAD_DEFINE(init_id, INIT_STACKSIZE, init, NULL, NULL, NULL, TASK_PRIORITY_INIT, 0, 0);
K_THREAD_DEFINE(luos_id, LUOS_STACKSIZE, luos, NULL, NULL, NULL, LUOS_PRIORITY_INIT, 0, 0);
K_THREAD_DEFINE(change_led_state_id, TASK_STACKSIZE, change_led_state, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);
K_THREAD_DEFINE(lock_led_id, TASK_STACKSIZE, lock_led, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);
*/

/*   //----- Proj 1  ----------------------------------------------------------------------------------------------------------
#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <string.h>
#include "main.h"
#include "gpio_l4xx.h"

// 1000 msec = 1 sec
#define SLEEP_TIME_MS 1000

// The devicetree node identifier for the "led0" alias.
#define LED0_NODE DT_ALIAS(led0)

// size of stack area used by each thread
#define INIT_STACKSIZE 1024
#define TASK_STACKSIZE 512

// scheduling priority used by each thread
#define TASK_PRIORITY_INIT 8
#define TASK_PRIORITY      7

#if DT_NODE_HAS_STATUS(LED0_NODE, okay)
    #define LED0  DT_GPIO_LABEL(LED0_NODE, gpios)
    #define PIN   DT_GPIO_PIN(LED0_NODE, gpios)
    #define FLAGS DT_GPIO_FLAGS(LED0_NODE, gpios)
#else
    / A build error here means your board isn't set up to blink an LED.
    #error "Unsupported board: led0 devicetree alias is not defined"
    #define LED0  ""
    #define PIN   0
    #define FLAGS 0
#endif

static bool thread_run    = false;
static struct device *dev = NULL;
static bool led_state     = true;
static bool led_toggle    = true;

void init(void)
{
    int ret;

    //Luos_Init();
    //Button_Init();

    dev = device_get_binding(LED0);

    if (dev == NULL)
    {
        return;
    }

    ret = gpio_pin_configure(dev, PIN, GPIO_OUTPUT_ACTIVE | FLAGS);
    if (ret < 0)
    {
        return;
    }
    thread_run = true;
}

void change_led_state(void)
{
    k_msleep(1000);
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
        k_msleep(1000);
    }
}

void lock_led(void)
{
    k_msleep(1000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        led_toggle = !led_toggle;
        k_msleep(6000);
    }
}

K_THREAD_DEFINE(init_id, INIT_STACKSIZE, init, NULL, NULL, NULL, TASK_PRIORITY_INIT, 0, 0);
K_THREAD_DEFINE(change_led_state_id, TASK_STACKSIZE, change_led_state, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);
K_THREAD_DEFINE(lock_led_id, TASK_STACKSIZE, lock_led, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);
*/

/*   //----- Proj 2  ----------------------------------------------------------------------------------------------------------
#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <string.h>
#include "main.h"
#include "gpio_l4xx.h"
#include "luos_engine.h"
#include "button.h"

// 1000 msec = 1 sec
#define SLEEP_TIME_MS 1000

// The devicetree node identifier for the "led0" alias.
#define LED0_NODE DT_ALIAS(led0)

// size of stack area used by each thread
#define INIT_STACKSIZE        1024 //128
#define TASK_STACKSIZE        128
#define LUOS_TASK_STACKSIZE   1024
#define BUTTON_TASK_STACKSIZE 256

// scheduling priority used by each thread
#define LUOS_TASK_PRIORITY   12
#define BUTTON_TASK_PRIORITY 11
#define INIT_PRIORITY        10
#define TASK_PRIORITY        7

#if DT_NODE_HAS_STATUS(LED0_NODE, okay)
    #define LED0  DT_GPIO_LABEL(LED0_NODE, gpios)
    #define PIN   DT_GPIO_PIN(LED0_NODE, gpios)
    #define FLAGS DT_GPIO_FLAGS(LED0_NODE, gpios)
#else
    // A build error here means your board isn't set up to blink an LED
    #error "Unsupported board: led0 devicetree alias is not defined"
    #define LED0  ""
    #define PIN   0
    #define FLAGS 0
#endif

static bool thread_run    = false;
static struct device *dev = NULL;
static bool led_state     = true;
static bool led_toggle    = true;

void init(void)
{
    int ret;

    Luos_Init();
    Button_Init();
    dev = device_get_binding(LED0);

    if (dev == NULL)
    {
        return;
    }

    ret = gpio_pin_configure(dev, PIN, GPIO_OUTPUT_ACTIVE | FLAGS);
    if (ret < 0)
    {
        return;
    }
    thread_run = true;
}

void change_led_state(void)
{
    k_msleep(1000);
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
        k_msleep(1000);
    }
}

void lock_led(void)
{
    k_msleep(1000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        led_toggle = !led_toggle;
        k_msleep(6000);
    }
}

void luos_thread(void)
{
    k_msleep(1000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        Luos_Loop();
        k_yield();
    }
}

void button_thread(void)
{
    k_msleep(1000);
    if (!thread_run)
    {
        return;
    }

    while (1)
    {
        Button_Loop();
        k_yield();
    }
}

K_THREAD_DEFINE(init_id, INIT_STACKSIZE, init, NULL, NULL, NULL, INIT_PRIORITY, 0, 0);
//K_THREAD_DEFINE(luos_id, LUOS_TASK_STACKSIZE, luos_thread, NULL, NULL, NULL, LUOS_TASK_PRIORITY, 0, 0);
//K_THREAD_DEFINE(button_id, BUTTON_TASK_STACKSIZE, button_thread, NULL, NULL, NULL, BUTTON_TASK_PRIORITY, 0, 0);
//K_THREAD_DEFINE(change_led_state_id, TASK_STACKSIZE, change_led_state, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);
//K_THREAD_DEFINE(lock_led_id, TASK_STACKSIZE, lock_led, NULL, NULL, NULL, TASK_PRIORITY, 0, 0);
*/
