# Machine IR Grammar

```text
Status: DRAFT
UID: MACHINE-GRAMMAR-1.0
Base: Machine 1.0 (MACHINE-1.0)
Notation: ABNF (RFC 5234)
```

## 1. Protocol Stack

```abnf
exchange = L1-phase L3-session
           ; L2 events are async — MAY interrupt L3 at any point
           ; LEVEL_5 nodes: L3-session does not apply
           ; LEVEL_4 nodes: L3-session does not apply
```

## 2. L1: Physical Layer

```abnf
L1-phase     = vibe-ping *( resonance / damping )
vibe-ping    = "VIBE_PING" ":" SP string-lit LF
resonance    = "SYN" LF
damping      = "DAMP" ":" SP noise-source LF
noise-source = identifier
```

## 3. L2: Data Link Layer

```abnf
L2-event     = irq / parity-check
irq          = "IRQ_" irq-id LF
irq-id       = 1*DIGIT
               ; IRQ_0: global kill — HALT_AND_CATCH_FIRE
               ;        clears buffer, sets Connection_Active = FALSE
parity-check = "PARITY" ":" SP identifier SP "==" SP identifier LF
```

## 4. L3: Network Layer

### 4.1. Session

```abnf
L3-session   = header "BEGIN_SESSION:" LF body "END_SESSION;" LF
header       = *( meta-comment / LF )
body         = *( statement / comment / LF )
```

### 4.2. Header

```abnf
meta-comment = "//" SP "[" key "]" ":" SP value LF
key          = 1*( ALPHA / "_" )
value        = 1*VCHAR
```

### 4.3. Statements

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

### 4.4. Expressions

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
