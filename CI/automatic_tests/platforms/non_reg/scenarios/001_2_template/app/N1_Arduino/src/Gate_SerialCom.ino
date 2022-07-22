
#include <Arduino.h>

#ifdef __cplusplus
extern "C"
{
#endif

#include <pipe.h>
#include <gate.h>
#include "luos_engine.h"
#include "N1_node_config.h"

void PTP_Power_Init(void);
void PTP_Power_Config(void);
#ifdef __cplusplus
}
#endif

void setup()
{
    PTP_Power_Init();
    Luos_Init();
    Gate_Init();
    Pipe_Init();

    PTP_Power_Config();
}

void loop()
{
    Luos_Loop();
    Gate_Loop();
    Pipe_Loop();
}


void PTP_Power_Init(void)
{
    pinMode(PTP_POWER_PIN, OUTPUT);
    digitalWrite(PTP_POWER_PIN, LOW);
}

void PTP_Power_Config(void)
{
    # ifdef PTP_POWER
    digitalWrite(PTP_POWER_PIN, HIGH);
    # else
    digitalWrite(PTP_POWER_PIN, LOW);
    # endif
}
