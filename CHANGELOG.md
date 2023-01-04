# Changelog

## [0.2.0](https://github.com/discatpy-dev/core/compare/v0.1.0...v0.2.0) (2023-01-04)


### ⚠ BREAKING CHANGES

* rewrite http ratelimiting ([#29](https://github.com/discatpy-dev/core/issues/29))
* rename impl module to utils
* **gateway.types:** remove unused convert_from_untyped function
* new snowflake helper class
* **dispatcher/event:** parent -> force_parent
* **Dispatcher:** add shortcut for adding callback to event

### Features

* add support for all gateway events ([4c4b200](https://github.com/discatpy-dev/core/commit/4c4b200e751272397874584ae9cc8bb3affe2b4a))
* **Dispatcher:** add shortcut for adding callback to event ([b6af38b](https://github.com/discatpy-dev/core/commit/b6af38bccdaa6785e1c73ad1ac783416687c41c0))
* **gateway.types:** remove unused convert_from_untyped function ([3338336](https://github.com/discatpy-dev/core/commit/3338336c47de75580498f9c77bc71f7f32534892))
* new snowflake helper class ([07b1ab3](https://github.com/discatpy-dev/core/commit/07b1ab3c38e7596531456e2d3f3ecfaa003a1c40))


### Bug Fixes

* compatbility w/ 3.9 ([bf58b9e](https://github.com/discatpy-dev/core/commit/bf58b9e901b9a90d1b3fb44f1aa2ce1477421769))
* **GatewayClient:** check if heartbeat_timeout is negative or 0 ([275b32f](https://github.com/discatpy-dev/core/commit/275b32f03c0d3e7350bd2bdc5122e5133f545e4d))
* GuildScheduledEventEntityMetadata was renamed ([bfb5e11](https://github.com/discatpy-dev/core/commit/bfb5e11596da5c23438440be36c4798d4774a360))
* heartbeat handler kept crashing for unknown reasons ([8b874f1](https://github.com/discatpy-dev/core/commit/8b874f1c99a3f8074d04bc17231683691e957795))
* numerous typing issues ([fcfaffe](https://github.com/discatpy-dev/core/commit/fcfaffe7baf96af82c5c558d51a406c24a9ac7c7))
* pyright errors ([#24](https://github.com/discatpy-dev/core/issues/24)) ([e5bacb8](https://github.com/discatpy-dev/core/commit/e5bacb8cd0d225182547619d6c3df4be845ddf67))
* ratelimiter assumed that bucket exists ([965891e](https://github.com/discatpy-dev/core/commit/965891e6c7dda35f88a6e24c3f33378e26794356))
* remove commented out code ([e0a1574](https://github.com/discatpy-dev/core/commit/e0a157434df37361ca57784a37deb4fdcde4363e))
* typing.NamedTuple does not support multiple inheritance ([e874747](https://github.com/discatpy-dev/core/commit/e8747476e0a14908df8d363e11cdbfb3dee0c35d))


### Code Refactoring

* **dispatcher/event:** parent -&gt; force_parent ([e662ddf](https://github.com/discatpy-dev/core/commit/e662ddfccab3e97fe53a7ddac32c61f1ae7240b4))
* rename impl module to utils ([a9c2f83](https://github.com/discatpy-dev/core/commit/a9c2f83c058ccade2e22867b99678ce1a9049400))
* rewrite http ratelimiting ([#29](https://github.com/discatpy-dev/core/issues/29)) ([03366dd](https://github.com/discatpy-dev/core/commit/03366ddfe20de8821caa13165788185a7c291e2c))
