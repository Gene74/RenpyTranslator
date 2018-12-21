RENPY-TRANSLATOR

The idea is to create a tool for foreign Ren'Py projects which have translation files.
The tool will now take those files, read the translations and translate the related scripts.

The logic works as follows:
1. Read the translation file -> complete translation string with " at beginning and end
2. Read the related script file
3. Replace/Tranlate all appearances
4. Create a backup of the original file (can be deactivated with -n)
5. Save the new script file

If the param -r is used the translation will be done in reverse.

Use with caution.
