TITLE Low-level I/O procedures   (Proj6-dobkinr.asm)

; Author:	Ryan Dobkin
; Last Modified: 3/17/24
; OSU email address: dobkinr@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number:   6      Due Date: 3/17/24
; Description: Takes n integer inputs from user, translates them from ASCII to decimal SDWORD, then back to ASCII.
; Displays all n inputs, sum of inputs, and truncated avg.

INCLUDE Irvine32.inc

; ---------------------------------------------------------------------------------
; Name: mGetString
;
; Get user input and display string in memory. - need to get count, readbytes working
;
; Preconditions: prompt = BYTE, input = DWORD, count = number
;
; Receives: prompt to print, input variable, count = total size
;
; returns: EAX = string in ASCII
; ---------------------------------------------------------------------------------
mGetString  MACRO prompt, input, readBytes
  ; stores used registers
  push  EAX
  push  EDX
  push  ECX
  ; Display prompt -prompt-
  mDisplayString prompt
  ; Sets ECX = max string size MAXSTRINGSIZE constant
  ; User input into -input-
  mov   ECX, 5
  mov   EDX, input
  call  ReadString
  mov   input, EDX
  ; Make sure string is <= MAXSTRINGSIZE
  cmp   EAX, MAXSTRINGSIZE
  jg    _Invalid
  ; output bytes read -readBytes- | irvine saves EAX as input string size
  mov   readBytes, EAX
  jmp   _LocalEnd
  ; restores used registers
  _LocalEnd:
  pop   EAX
  pop   EDX
  pop   ECX
ENDM

; ---------------------------------------------------------------------------------
; Name: mDisplayString
;
; Print the string stored in a passed memory location.
;
; Preconditions: Parameter must be OFFSET of string.
;
; Receives: input = string
;
; returns: None.
; ---------------------------------------------------------------------------------
mDisplayString  MACRO input ; DONE
  ; stores used registers
  push  EDX
  ; moves -input- to EDX, prints
  mov   EDX, input
  call  WriteString
  ; restores used registers
  pop   EDX
ENDM


TESTSIZE = 10
CMPLO = 48
CMPHI = 57
MAXSTRINGSIZE = 4
ISNEGATIVE = 45
ISPOSITIVE = 43

.data

readArray   SDWORD TESTSIZE DUP(?)
inputStr    DWORD 1 DUP(?)
sumElement  SDWORD 1 DUP(?)
sumNumber   SDWORD 1 DUP(?)
readBytes   DWORD ?
format0     BYTE ", ",0
prompt0     BYTE "PROJECT 6 - Low-Level I/O Procedures",10
prompt1     BYTE "Written by: Ryan Dobkin",10,10,0
prompt2     BYTE "Please enter 10 signed integers. "
prompt3     BYTE "Each number must fit inside a 32 bit register. ",10
prompt4     BYTE "After you finish your inputs, I will display the integers, along with their sum and average value.",10,10,0
prompt5     BYTE "Please enter a signed integer: ",0
prompt6     BYTE "Invalid. Your number was either unsigned or too big. Please enter a valid number: ",0
prompt7     BYTE "You entered the following integers: ",0
prompt8     BYTE "The sum of your integers is: ",0
prompt9     BYTE "The truncated average of your integers is: ",0
prompt10    BYTE "Thanks for playing! Goodbye.",0

.code
main PROC
  mDisplayString    OFFSET prompt0      ; introduction
  mDisplayString    OFFSET prompt2
  mov   EDI, OFFSET readArray
  mov   ECX, TESTSIZE                   ; sets ecx (loop counter) to TESTSIZE (10)
  _readLoop:                            ; iterates through _readLoop and prompts input until array is full (10)
    push    EDI
    push    OFFSET readBytes
    push    OFFSET inputStr
    push    OFFSET prompt5
    push    OFFSET prompt6
    call	ReadVal
    pop     EDI
    mov     EAX, inputStr
    stosd                               ; moves passed integer into readArray, increments
    loop	_readLoop
  ; displays array of integers
  mov     ESI, OFFSET readArray
  mov     ECX, TESTSIZE
  call    CrLf
  mDisplayString  OFFSET prompt7
  _displayList:
    push    ECX
    mov     EAX, [ESI]
    mov     inputStr, EAX
    push    ESI
    push    OFFSET inputStr
    call    WriteVal
    mDisplayString  OFFSET format0
    pop     ESI
    pop     ECX
    add     ESI, 4
    loop    _displayList
  call  CrLf
  call  CrLf
  push  OFFSET sumNumber
  push  OFFSET sumElement
  push  OFFSET prompt8
  push  OFFSET readArray
  call  SumList                         ; displays sum of array
  call  CrLf
  call  CrLf
  push  OFFSET sumNumber
  push  OFFSET prompt9
  call  AvgList                         ; displays the truncated avg of the array
  call  CrLf
  call  CrLf
  mDisplayString    OFFSET prompt10     ; goodbye message
	Invoke ExitProcess,0	            ; exit to operating system
main ENDP

; ------------------------------------------------------------------------------------------------
; Name: ReadVal
;
; Gets user input via mGetString, converts from ASCII to numberic value DWORD,
; validates input to check for invalid letters, symbols, or other non-integers,
; and stores the value in a passed memory variable.
;
; Preconditions: mGetString exists, input is string, passed valid variable.
;
; PostConditions: inputStr set to input
;
; Receives: input = input string, output = variable for storage.
;
; Returns: converted integer.
; ------------------------------------------------------------------------------------------------
ReadVal PROC
  ; sets stack frame
    push	EBP
    mov	    EBP, ESP
    push    ECX
  ; sets up for intro prompt
    mov     EBX, 0
    mov     EDX, [EBP+12] 
    mov     ECX, 0
    push    ECX
  _Start:
  ; mGetString  prompt, inputStr, actualInput
    mGetString  EDX, [EBP+16], [EBP+20]
    pop     ECX
    mov     ESI, [EBP+16]                   ; make passed string element ESI, then iterate through [ESI] until null terminator
    _Converter:
    push    EBX
    lodsb
    ; checks if valid
    cmp     al, ISNEGATIVE
    je      _NegativeLoop
    cmp     al, ISPOSITIVE
    je      _NegativeLoop
    cmp     al, CMPLO
    jl      _Invalid
    cmp     al,  CMPHI                      ; compares element to 57, [57h = 9]
    jg      _Invalid
    sub     al, CMPLO                      ; subtracts 48 from input after confirming it is a num. Translates EAX from ASCII hex to integer.
    ; now that char n is in decimal and valid, ECX*10 then add al
    movsx   EBX, al
    mov     EAX, ECX
    mov     EDX, 10
    mul     EDX
    add     EAX, EBX
    mov     ECX, EAX
    pop     EBX
    inc     EBX
    mov     EDX, [EBP+20]
    cmp     EBX, EDX
    jl      _Converter
    jmp     _End
  _Invalid:
    mov     EDX, [EBP+8]
    jmp     _Start
  _End:
    push    EAX
    mov     EDI, [EBP+16]
    mov     ESI, [EBP+16]
    lodsb
    cmp     al, ISNEGATIVE
    je      _Invert
    mov     EAX, ECX
    stosd
    jmp     _NReturn
  _Invert:
    neg     ECX
    mov     EAX, ECX
    stosd   
    jmp     _NReturn
  _NegativeLoop:
    inc     EBX
    jmp     _Converter
  _NReturn:
    pop     EAX
    pop     ECX
    pop	    EBP
    ret     16
ReadVal ENDP

; ------------------------------------------------------------------------------------------------
; Name: WriteVal
;
; Convert SDWORD to string of ASCII characters,
; then, invoke mDisplayString to print the output.
;
; Preconditions: First pushed parameter is OFFSET of string to be converted, printed.
;
; PostConditions: Prints given value in offset
;
; Receives: OFFSET of value to print, up to 4 digits long
;
; Returns: None
; ------------------------------------------------------------------------------------------------
WriteVal PROC
; sets stack frame
  push	EBP
  mov	EBP, ESP
; Gets passed SDWORD integer
  mov   ESI, [EBP+8]
  mov   EAX, [ESI]
  mov   ECX, 4
  mov   EBX, 0
  _Converter:
  shl   EBX, 8
  push  ECX
  cmp   EAX, ISNEGATIVE
  je    _AddNegative
  mov   EDX, 0
  mov   ECX, 10
  div   ECX
  add   EDX, 48              ; adds 48 to convert back to ASCII value
  ; need to find way to stop it
  or    EBX, EDX
  pop   ECX
  loop  _Converter
  shr   EBX, 8
  _EndWrite:
    mov     EDI, [EBP+8]
    mov     EAX, EBX
    stosd
    mov     EAX, [EBP+8]
    mDisplayString  [EBP+8]
    pop	    EBP
    ret	    4
  _AddNegative:
    mov EBX, ISNEGATIVE
    shl EBX, 8
WriteVal ENDP

; ------------------------------------------------------------------------------------------------
; Name: SumList
;
; Iterates through the passed array and adds all elements, then displaysd the total sum.
;
; Preconditions: The passed aray is TYPE (S)DWORD.
;
; PostConditions: None.
;
; Receives: SDWORD array at offset [EBP+8], variable to send sum to write [EBP+16], variable to use sum in avg proc [EBP+20], prompt [EBP+12]
;
; Returns: [EBP+20] variable containing the sum.
; ------------------------------------------------------------------------------------------------
SumList PROC
  ; sets stack frame
  push	EBP
  mov	EBP, ESP
  ; Displays prompt
  mDisplayString   [EBP+12]
  ; moves convertedList -> ESI
  mov   ESI, [EBP+8]
  mov   ECX, TESTSIZE
  mov   EAX, 0
  mov   EDX, 0
  _addList:
    mov     EAX, [ESI]
    add     EDX, EAX    
    add     ESI, 4
    loop    _addList
  mov   ESI, [EBP+20]
  mov   [ESI], EDX
  mov   ESI, [EBP+16]
  mov   [ESI], EDX
  push  [EBP+16]
  call  WriteVal
  pop	EBP
  ret	12
SumList ENDP

; ------------------------------------------------------------------------------------------------
; Name: AvgList
;
; Iterates through and takes the average of the array, then prints the truncated average.

; Preconditions: the passed sum is an offset, and is [EBP+12]
;
; PostConditions: None.
;
; Receives: offset of pre-caluclated sum of array, constant of number of elements in the array.
; offset of prompt to print.
;
; Returns: None.
; ------------------------------------------------------------------------------------------------
AvgList PROC
  ; sets stack frame
  push	EBP
  mov	EBP, ESP
  ; Displays prompt
  mDisplayString [EBP+8]
  mov   ESI, [EBP+12]
  mov   edx, 0
  mov   eax, [ESI]
  mov   ecx, TESTSIZE
  div   ecx
  mov   ESI, [EBP+12]
  mov   [ESI], EAX
  push  [EBP+12]
  call  WriteVal
  ; return
  pop	EBP
  ret	8
AvgList ENDP

END main
