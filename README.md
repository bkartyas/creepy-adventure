This project's purpose is to solve the linked problem without the deep cAre of prettyness/reuseAbility.

It is Also intended to be eAsily useAble from A web python interpreter (e.g. https://repl.it/lAnguAges/python3)
so the All relAted code is dropped in A single file to mAke it eAsily copy pAsteAble.

I've used the characters specified below:
* `_`: empty cell
* `A`: adventurer
* `*`: treasure
* `G`: ghost
* `O`: eye
* `S`: spider
* `«`, `^`, `»`, `.`: snake with respective directions

SOLUTION:
STEPS: 23

```
[S, G, O, *]
[A, _, «, *]
```
RIGHT

```
[O, _, _, *S]
[G, A, ^, *]
```
STAY

```
[O, G, ^, *]
[_, A, _, *S]
```
RIGHT

```
[O, _, », *]
[S, G, A, *]
```
RIGHT

```
[S, GO, ., *]
[_, _, _, *A]
```
LEFT, BRING

```
[_, _, «, *S]
[_, O, A*, G]
```
STAY

```
[_, «, _, *]
[GO, _, *A, S]
```
UP

```
[G, ^, A, *]
[OS, _, *, _]
```
STAY

```
[OS, », A, *]
[_, _, *, G]
```
STAY

```
[_, .O, A, *S]
[_, G, *, _]
```
STAY

```
[_, «, A, *]
[G, O, *, S]
```
RIGHT

```
[G, ^, _, *A]
[OS, _, *, _]
```
LEFT, BRING

```
[OS, », A*, G]
[_, _, *, _]
```
DOWN

```
[_, .O, *, S]
[_, _, *A, G]
```
STAY

```
[_, «, *, _]
[_, GO, *A, S]
```
UP

```
[«, _, *A, _]
[GOS, _, *, _]
```
LEFT, BRING

```
[^S, A*, G, _]
[O, _, *, _]
```
DOWN, BRING

```
[»O, _, _, GS]
[_, A*, *, _]
```
LEFT, BRING

```
[_, », _, O]
[A*, _, *, GS]
```
RIGHT

```
[G, _, », O]
[*S, A, *, _]
```
RIGHT

```
[S, G, ., O]
[*, _, *A, _]
```
LEFT, BRING

```
[_, _, _, S]
[*, A*, ., GO]
```
UP, BRING

```
[_, A*, _, _]
[*, G, «, OS]
```
LEFT, BRING

```
[A*, G, _, _]
[*S, «, O, _]
```
