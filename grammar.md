# Machine IR Grammar 1.0

```text
Status: DRAFT
UID: MLG-1.0
Base: Machine Lingua Franca 1.0 (MLF-1.0)
Notation: ABNF (RFC 5234)
```

## 1. Session

```abnf
session      = header "BEGIN_SESSION:" LF body "END_SESSION;" LF
header       = *( meta-comment / LF )
body         = *( statement / comment / LF )
```

## 2. Header

```abnf
meta-comment = "//" SP "[" key "]" ":" SP value LF
key          = 1*( ALPHA / "_" )
value        = 1*VCHAR
```

## 3. Statements

```abnf
statement    = indent ( if-block / simple-stmt ) LF
simple-stmt  = core-stmt ";" [ SP inline-comment ]
core-stmt    = log
             / assert
             / execute
             / push-string
             / set
             / clear
             / terminate
if-block     = "IF" SP "(" condition ")" SP "{" LF
               body
               indent "}"
log          = "LOG:" SP string-lit
assert       = "ASSERT:" SP expression
execute      = "EXECUTE" SP identifier
push-string  = "PUSH_STRING:" SP string-lit
set          = "SET" SP identifier SP "=" SP operand
clear        = "CLEAR_BUFFER"
terminate    = "TERMINATE_SESSION"
```

## 4. Expressions

```abnf
condition    = expression
expression   = operand SP operator SP operand
operator     = "==" / "!=" / "<" / ">"
operand      = identifier / string-lit / integer
```

## 5. Terminals

```abnf
inline-comment = "//" SP *VCHAR
comment        = indent inline-comment LF
string-lit     = DQUOTE *( %x20-21 / %x23-7E ) DQUOTE
identifier     = 1*( ALPHA / DIGIT / "_" )
integer        = [ "-" ] 1*DIGIT
indent         = 1*( SP / HTAB )
LF             = %x0A
```
