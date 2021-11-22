/******************************************************************************
 * @file gate
 * @brief Service gate
 * @author Luos
 ******************************************************************************/
#include <stdio.h>
#include <stdbool.h>
#include "assert_app.h"

/*******************************************************************************
 * Definitions
 ******************************************************************************/
#define ASSERT_FREQ    1000
#define MAX_ASSERT_MSG 5
/*******************************************************************************
 * Variables
 ******************************************************************************/
service_t *assert_app;
uint32_t assert_timer  = 0;
uint8_t assert_counter = 0;
/*******************************************************************************
 * Function
 ******************************************************************************/
static void Assert_MsgHandler(service_t *service, msg_t *msg);
/******************************************************************************
 * @brief init must be call in project init
 * @param None
 * @return None
 ******************************************************************************/
void Assert_Init(void)
{
    revision_t revision = {.major = 1, .minor = 0, .build = 0};
    // inspector service creation
    assert_app = Luos_CreateService(Assert_MsgHandler, LUOS_LAST_TYPE, "assert_app", revision);
}

/******************************************************************************
 * @brief loop must be call in project loop
 * @param None
 * @return None
 ******************************************************************************/
void Assert_Loop(void)
{
    // check if the network is detected
    if (Luos_IsNodeDetected())
    {
        if ((Luos_GetSystick() - assert_timer >= ASSERT_FREQ) && (assert_counter < MAX_ASSERT_MSG))
        {
            // Send a fake assert message each second
            msg_t msg;
            msg.header.target      = BROADCAST_VAL;
            msg.header.target_mode = BROADCAST;
            msg.header.cmd         = ASSERT;
            msg.header.size        = 1;
            // The data[0] is the number of the assert message counter for debugging purposes
            msg.data[0] = assert_counter;
            // send message
            Luos_SendMsg(assert_app, &msg);
            // reinitialize timer
            assert_timer = Luos_GetSystick();
            assert_counter++;
        }
    }
    else
    {
        // initialiaze timer and counter if a detection has occured
        assert_timer   = Luos_GetSystick();
        assert_counter = 0;
    }
}

static void Assert_MsgHandler(service_t *service, msg_t *msg)
{
}
