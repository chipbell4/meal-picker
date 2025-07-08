tell application "Reminders"
	activate
	tell list "%LIST%"
		make new reminder at end with properties { name: "%ITEM%", body: "%NOTE%" }
	end tell
end tell
