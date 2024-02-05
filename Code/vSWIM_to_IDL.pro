pro vswim_csv_to_sav, fin, fout 
;;;; reads CSV files from vSWIM and converts them into IDL sav files. 
;;; fin=full path to input filename ending in .csv, fout=full path to output file ending in .sav
;;; WRITTEN BY K. G. HANLEY on February 5th, 2023

if n_elements(fout) eq 0 then begin
  tmp=strsplit(fin,'.',/extract)
  fout=tmp[0]+'.sav'
endif

;;; read in the file 
result=read_csv(fin, header=header) 
    
    ;;; fix the date labels since they have brackets in the csv 
    header[1]='date_utc'
    header[2]='date_unix'
    
    ;;; skip the 0th column which just counts the # of records
    ;;; pull out the headers into variables
    ;;; need separate loops for <9 and >9 because of the 0 in the field #
for field=1,8 do tmp=execute(header[field]+'=result.field0'+strtrim(field+1,2))
for field=9,44 do tmp=execute(header[field]+'=result.field'+strtrim(field+1,2))

;;; make all the columns into a string so you can save the variables 
var_string=''
for field=1,44 do var_string=var_string+header[field]+','

tmp=execute('save,'+var_string+'filename=fout')

if tmp then print, 'Success' else print, 'Save failed'
end
