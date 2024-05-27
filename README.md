# FlatBuffers Encoding and Decoding

## Introduction

This project demonstrates how to encode and decode data using FlatBuffers. The project includes:
- A Python script to encode data.
- A Python program to decode data.

## Schema Definition

The schema (`client.fbs`) defines a `Person`, a `Group`, and a union `Client` that can be either a `Person` or a `Group`.

## Prerequisites

- Python 3
- FlatBuffers library

## Setup

### 1. Install FlatBuffers

#### Python
```sh
pip install flatbuffers
