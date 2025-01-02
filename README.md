# Miscellaneous Tools
This repository is meant to hold simple, one-file Python tools of various kinds to be copied into projects as needed.

Some of the tools are my own, usually the simple and stupid ones. Other tools have been taken or adapted from other authors (see docstrings for attributions, where applicable).

## Arithmology

Convert between integers and certain number words, e.g. "tertial" -> 3, "triad" -> 3, "heptatonic" -> 7, "quadruple" -> 4; (7, 'polyad') -> "heptad", (5, 'cardinal') -> "five"

## Humps 

Convert strings between various case systems, e.g. "snake_case", "PascalCase", "camelCase", "kebab-case" (modified from original by github.com/nficano)

## Lexer

A simple lexer to convert text into tokens. A simplified version of the lexer at https://github.com/lark-parser/lark/blob/master/lark/lexer.py with a few modifications.

## Numerus

Convert between Indian and Roman numerals, e.g. 'MDCCCLVII' -> 1858

## Parsing

Boilerplate code for building hand-rolled tokenizers and parsers. Really only meant for situations where you have to parse a relatively small language.