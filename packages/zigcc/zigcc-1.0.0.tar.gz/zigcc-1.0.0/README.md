# zigcc

[![](https://github.com/jiacai2050/zig-cc/actions/workflows/ci.yml/badge.svg)](https://github.com/jiacai2050/zig-cc/actions/workflows/ci.yml)
[![](https://github.com/jiacai2050/zig-cc/actions/workflows/zig.yml/badge.svg)](https://github.com/jiacai2050/zig-cc/actions/workflows/zig.yml)
[![](https://github.com/jiacai2050/zig-cc/actions/workflows/release.yml/badge.svg)](https://github.com/jiacai2050/zig-cc/actions/workflows/release.yml)
[![](https://img.shields.io/pypi/v/zigcc.svg)](https://pypi.org/project/zigcc)

Util scripts aimed at simplifying the use of `zig cc`{.verbatim} for
compiling C, C++, Rust, and Go programs.

# Why

In most cases, we can use following command to use Zig for compile

``` bash
CC='zig cc' CXX='zig c++' ...
```

However in real world, there are many issues this way, such as:

-   [zig cc: parse -target and -mcpu/-march/-mtune flags according to
    clang #4911](https://github.com/ziglang/zig/issues/4911)
-   [Targets compare: Rust to
    Zig](https://gist.github.com/kassane/446889ea1dd5ff07048d921f2b755e78)
-   [unsupported linker
    arg](https://github.com/search?q=repo%3Aziglang%2Fzig+unsupported+linker+arg%3A&type=issues)
-   [Rust + \`zig cc\` CRT conflict. :
    rust](https://www.reddit.com/r/rust/comments/q866qx/rust_zig_cc_crt_conflict/)

So this project was born, it will

-   Convert target between Zig and Rust/Go
-   Ignore link args when `zig cc`{.verbatim} throw errors, hopefully
    this will make compile successfully, WIP.

# Install

``` bash
pip3 install -U zigcc
```

This will install three executables:

-   `zigcc`{.verbatim}, used for `CC`{.verbatim}
-   `zigcxx`{.verbatim}, used for `CXX`{.verbatim}
-   `zigcargo`{.verbatim} can used to replace `cargo`{.verbatim}, it
    will automatically set
    -   `CC`{.verbatim} `CARGO_TARGET_<triple>_LINKER`{.verbatim} to
        `zigcc`{.verbatim}
    -   `CXX`{.verbatim} to `zigcxx`{.verbatim}

# Use in GitHub Action

Adding a step to your workflow like this:

``` yaml
- name: Install zigcc
  uses: jiacai2050/zigcc@v1
  with:
    zig-version: master
```

Then you can invoke `zigcc`{.verbatim} `zigcxx`{.verbatim}
`zigcargo`{.verbatim} in following steps.

# Config

There some are env variable to config zigcc:

-   `ZIGCC_FLAGS`{.verbatim}, space separated flags, pass to zig cc. An
    example is set this to `-fno-sanitize=undefined`{.verbatim} to
    disable sanitize since they may break your programs. See [Catching
    undefined behavior with zig
    cc](https://nathancraddock.com/blog/zig-cc-undefined-behavior/)

-   `ZIGCC_BLACKLIST_FLAGS`{.verbatim}, space separated flags, used to
    filter flags `zig cc`{.verbatim} don\'t support, such as
    `-Wl,-dylib`{.verbatim} otherwise you could see errors below

    ``` bash
    note: error: unsupported linker arg: -dylib
    ```

-   `ZIGCC_VERBOSE`{.verbatim} Set to `1`{.verbatim} enable verbose
    logs.
