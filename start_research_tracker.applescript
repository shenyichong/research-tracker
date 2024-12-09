tell application "Terminal"
    set currentPath to POSIX path of ((path to me as text) & "::")
    do script "cd " & quoted form of currentPath & " && ./start_research_tracker.command"
end tell 