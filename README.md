py-sprinkler
====================


File contents JSON structure
----------------------------

> {
>	// The default sprinkler fallback schedule,
>	// if no day / month matches.
>	default: {
>
>		// All schedules, in no particular order
>		schedules: [
>			{ 
>				// The pin number, according to
>				// GPIO raspberry numbering scheme
>				pinNumbers: [17, 13, ...], 
>				// The number of seconds from 12
>				// am;
>				start: 21600, `(6 am)`
>				// The number of seconds to run
>				duration: 600 `(10 minutes)`
>			}
>           ... other schedules, for the same or 
>               other pin configurations.
>
>		]
>
>	}
>}

