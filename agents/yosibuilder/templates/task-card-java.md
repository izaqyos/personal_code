id: J1
title: feat(text): add slugify
edit: src/main/java/com/example/text/Slugs.java src/test/java/com/example/text/SlugsTest.java
test: ./gradlew test --tests com.example.text.SlugsTest --offline -q
lint: ./gradlew checkstyleMain spotbugsMain --offline -q
---
Goal: one sentence on what this card delivers.

## Design (implement exactly these, nothing more)

    public final class Slugs { public static String slugify(String text, int maxLen) }  // IllegalArgumentException if maxLen < 1

## Test plan (write exactly these tests in SlugsTest, JUnit 5)

void joinsWordsWithDashes()
void truncatesWithoutTrailingDash()
void rejectsNonPositiveMaxLen()
