# monapp
monitor display if unplug will shutdown computer for set time

For PisoNet/Vendo users that needs to turnoff PC after a set of minutes
No need to connect the Computer in Vendo just the Monitor
for HDMI/DP Monitor only, not working in VGA

0. install python
1. run monapp.py for ininital run and to check if your monitor is compatible
2. rename to monapp.pyw to run without console
3. put it in the startup folder to run on boot with the config.json
4. adjust to your preferences
{
    "check_interval_seconds": 2,
    "shutdown_delay_seconds": 10
}
