Sub CustomCase()
    Dim oSheet As Object ' Sheet object
    Dim oRange As Object ' ScCellRangeObj
    Dim oCell As Object ' Cell object
    Dim s As String ' Cell value
    Dim i As Integer ' Loop variable
    
    ' Get the active sheet
    oSheet = ThisComponent.CurrentController.ActiveSheet
    
    ' Get the selected range
    oRange = ThisComponent.CurrentSelection
    
    ' Loop through each cell in the range
    For i = 0 To oRange.Rows.Count - 1
        For j = 0 To oRange.Columns.Count - 1
            oCell = oRange.GetCellByPosition(j, i)
            ' Check if the cell contains text
            If oCell.Type = 2 Then
                s = oCell.String ' Get the cell value as string
                s = CustomCaseLogic(s) ' Apply custom case logic
                oCell.String = s ' Assign the modified string back to the cell
            End If
        Next j
    Next i
End Sub

Function CustomCaseLogic(s As String) As String
    Dim result As String ' Result string
    Dim c As String ' Current character
    Dim inPredicate As Boolean ' Flag to track if inside a predicate
    Dim lowerNext As Boolean ' Flag to track if next character should be lowercase
    Dim i As Integer ' Loop variable
    
    result = ""
    inPredicate = False
    lowerNext = False
    
    ' Loop through each character in the string
    For i = 1 To Len(s)
        c = Mid(s, i, 1) ' Get the current character
        
        If (inPredicate Or lowerNext) And IsAlpha(c) Then
            c = LCase(c) ' Convert to lowercase
            lowerNext = False
        ElseIf c = "∀" Or c = "∃" Then
            lowerNext = True
        ElseIf Not inPredicate And IsAlpha(c) Then
            inPredicate = True
        ElseIf Not IsAlpha(c) Then
            inPredicate = False
        End If
        
        result = result & c ' Append the modified character to the result string
    Next i
    
    CustomCaseLogic = result
End Function

Function IsAlpha(c As String) As Boolean
    IsAlpha = (c Like "[A-Za-z]")
End Function
