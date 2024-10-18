# TAP-Consumer CHANGELOG
## 0.0.4 (2024-10-18)


### Fixes


* fix: no longer print TAP version in summary — rjdbcm <rjdbcm@outlook.com>
([`1ae30bc`](https://github.com/OZI-Project/TAP-Consumer/commit/1ae30bc41b110c8c29cfc60749a15f2d2433229b))

* fix: add support for subtests — rjdbcm <rjdbcm@outlook.com>
([`cb4e572`](https://github.com/OZI-Project/TAP-Consumer/commit/cb4e5725f6a8a032a77f670d48c65251e1ac9852))


### Performance improvements


* perf: add stubs — rjdbcm <rjdbcm@outlook.com>
([`6ab1b0b`](https://github.com/OZI-Project/TAP-Consumer/commit/6ab1b0b43b9ed848448b7d8ecb13596acdfcf211))

* perf: add docstrings — rjdbcm <rjdbcm@outlook.com>
([`2400dde`](https://github.com/OZI-Project/TAP-Consumer/commit/2400dde14e2a43d9d4a82a3a7e8ac0326543a4c5))

* perf: refactor to allow method chaining — rjdbcm <rjdbcm@outlook.com>
([`057c5d0`](https://github.com/OZI-Project/TAP-Consumer/commit/057c5d0ed4e8fd894f4cffff149a02516fee4304))

## 0.0.3 (2024-10-17)


### Fixes


* fix: bail out is now caseless — rjdbcm <rjdbcm@outlook.com>
([`eb7b17e`](https://github.com/OZI-Project/TAP-Consumer/commit/eb7b17ec26b1d713fc5f9f396b5c1a6ba40720bc))

## 0.0.2 (2024-10-17)


### Fixes


* fix: stop dumping raw test results — rjdbcm <rjdbcm@outlook.com>
([`8d67172`](https://github.com/OZI-Project/TAP-Consumer/commit/8d67172f4718643e7680b19f0737c287927348a3))


### Performance improvements


* perf: add YAML diagnostics summary — rjdbcm <rjdbcm@outlook.com>
([`7a1f27a`](https://github.com/OZI-Project/TAP-Consumer/commit/7a1f27a51bb171e28ab26ea1c798b143709dc609))

## 0.0.1 (2024-10-16)


### Fixes


* fix: broken symlink — rjdbcm <rjdbcm@outlook.com>
([`f32e67b`](https://github.com/OZI-Project/TAP-Consumer/commit/f32e67ba0a07551e0c36ff791809369b373363a2))

* fix: add MIT notice — rjdbcm <rjdbcm@outlook.com>
([`1e91d29`](https://github.com/OZI-Project/TAP-Consumer/commit/1e91d2948926a26b343e866b473c2b58d188c5f6))

* fix: dowload link — rjdbcm <rjdbcm@outlook.com>
([`6f5a145`](https://github.com/OZI-Project/TAP-Consumer/commit/6f5a14593b959a26462a58c67d700ef267e540de))

* fix: add PyYAML as a dependency — rjdbcm <rjdbcm@outlook.com>
([`85ad9a0`](https://github.com/OZI-Project/TAP-Consumer/commit/85ad9a0826990c6da1ccfd39bf99dae4b2f82b37))


### Performance improvements


* perf: clean up code — rjdbcm <rjdbcm@outlook.com>
([`16721f1`](https://github.com/OZI-Project/TAP-Consumer/commit/16721f1cd280af292237e09dde1383929189db0e))

* perf: clean up code — rjdbcm <rjdbcm@outlook.com>
([`6928f06`](https://github.com/OZI-Project/TAP-Consumer/commit/6928f06be492789a2449ff088ebfc80b3ab0bd81))

* perf: clean up code — rjdbcm <rjdbcm@outlook.com>
([`a249968`](https://github.com/OZI-Project/TAP-Consumer/commit/a2499682a0affcb88e892cd9b17138bfa6cc4ba4))

* perf: add tests — rjdbcm <rjdbcm@outlook.com>
([`b7e0be3`](https://github.com/OZI-Project/TAP-Consumer/commit/b7e0be36a3a7f56ff4f49df5a5a24956824d88cd))

* perf: initial commit — rjdbcm <rjdbcm@outlook.com>
([`52ee1f1`](https://github.com/OZI-Project/TAP-Consumer/commit/52ee1f17fecc982da3dcd5ed8fab40f28eda6ce5))


### Unknown


* Update README.rst — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`6198307`](https://github.com/OZI-Project/TAP-Consumer/commit/6198307048b4004552ecd6cc9ad964760bcea792))


## 0.0.0 (2024-10-15)

### :tada:

* :tada:: Initialized TAP-Consumer with ``ozi-new``.

```sh
ozi-new project --name TAP-Consumer --github-harden-runner --github-harden-runner --enable-uv --enable-uv --no-strict --no-strict --summary 'Parses and serializes Test Anything Protocol output.' --keywords TAP,testing,unittest --home-page https://oziproject.dev --author 'Eden Ross Duff MSc' --author-email help@oziproject.dev --license 'OSI Approved :: Apache Software License' --license-expression 'Apache-2.0 WITH LLVM-exception' --requires-dist pyparsing --requires-dist prompt-toolkit
```