# CHANGELOG

PyPI grscheller.untyped project: OBSOLETED!

## Releases and Important Milestones

### Version 0.4.1 - PyPI Release: 2024-10-17

* Obsoleted PyPI project
  * use grscheller.experimental instead
    * corresponds to grscheller.experimental version 0.1.0
  * decided to use with strict typing
    * hence a name change was essential
    * did not want to put back in grscheller.fp
      * having both classes Nada and MB there redundant
      * still want to preserve this implementation

### Version 0.4.0 - PyPI Release: 2024-10-03

* API change
  * changed method name `Nada.nget` to `Nada.nada_get`
    * a little more inconvenient, but less likely of a name collision

### Version 0.3.0 - PyPI Release: 2024-10-02

* renamed untyped.nothing to untyped.nada
  * Nothing -> Nada
  * nothing -> nada

### Version 0.2.0 - PyPI Release: 2024-08-17

* typing improvements back-ported from grscheller.fp
* updated optional dependencies to use grscheller.circular-array 3.4.0
  * for tests/

### Version 0.1.1 - PyPI Release: 2024-08-12

* prototype of a module level inaccessible sentinel value
  * _nothing_nada: _Nothing_Nada
  * for use only within the grscheller.untyped module itself

### Version 0.1.0 - Initial PyPI Release: 2024-08-08

* moved module nothing from grscheller.fp
  * wanted everything in grscheller.fp strictly typed
  * felt class Nothing worked better untyped
    * at least marginally typed with Any
