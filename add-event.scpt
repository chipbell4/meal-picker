-- Format is "8/25/2025 at 1:00pm"
set startTime to date "%WHEN%"
set endTime to startTime + (1 * hours)

tell application "Calendar"
	tell calendar "Meals"
		make new event with properties {summary:"%SUMMARY%", description: "%DESCRIPTION%", start date: startTime, end date: endTime}
	end tell
end tell


date "8/25/2025 at 1:00pm"