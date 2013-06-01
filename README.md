py-sprinkler
====================


Required dependencies
---------------------
* GPIO -  run it on raspberry
* pyyaml - parse the configuration file

You can either have them downloaded/installed or use a python package manager (in my case, `pip`):
> sudo pip install pyyaml

_gpio is bundled in `Raspberry`'s OS (downloaded from their site)._


File contents JSON structure
----------------------------

```javascript
{
  // Configuration file - mainly the place to specify pid,
  // but other runtime arguments could be placed here.
  configurationFile: 'configuration.yaml'

  // The default sprinkler fallback schedule,
  // if no day / month matches.
  default: {
	  // All schedules, in no particular order
		schedules: [
		  { 
			  // The pin number, according to
				// GPIO raspberry numbering scheme
				pinNumbers: [17, 13, ...], 
				// The number of seconds from 12
				// am;
				start: 21600, // 6 am
				// The number of seconds to run
				duration: 600 // 10 minutes
			}
        //   ... other schedules, for the same or 
        //       other pin configurations.
		]

	}
}
```

Cron job scheduler
------------------
You need to added the following configuration to cron, in order to root users `crontab`:
`*/5 * * * * python /home/pi/sprinkler/check_time.py /home/pi/sprinkler/defaults.json`

Of course, arguments can be changed accordingly (the script above will check every 5 minutes of every hour, and locate the sprinkler's check_time.py in user's home directory).
