# WTC-Code-Clinics
WTC team 13

Configuration and setup:

1. run 'python3 code_clinic.py' in your terminal
  -You will be redirected to your browser where you must select your WeThinkCode
  Gmail account so the application may access your Google calendar. Follow prompts.

2. You will be asked to enter in:
  -username
  -location - cpt/jhb
  -amount of days for calendar pull
  -calendar name - team 13 calendar (or shared code clinic calendar)

3. You should now be all setup to use the code clinic tool!

4. Here is a list of commands available to use that can be used in the
   code-clinic booking programme:
   wtc-clinic [command arg]

    python3 code_clinic.py -v or --volunteer -date "yyyy-mm-dd" -time "HH:MM" -e "enter description here"
    python3 code_clinic.py -b or --book -id "xxx" -e "enter description here"
    python3 code_clinic.py -c or --cancel -id "xxx"
    python3 code_clinic.py -d or --delete -id "xxx"
    python3 code_clinic.py -r or --retrieve
    python3 code_clinic.py -p or --personal
    python3 code_clinic.py -u -days "enter a number here"
    python3 code_clinic.py-h or --help
        
    *For detailed information on what each command does, just add the single 
    letter flag to -h.
    e.g for more help on:
    -v --> python3 code_clinic.py -hv
    -b --> python3 code_clinic.py -hb
    -c --> python3 code_clinic.py -hc
    -d --> python3 code_clinic.py -hd
    -r --> python3 code_clinic.py -hr
    -p --> python3 code_clinic.py -hp
    -u --> python3 code_clinic.py -hu