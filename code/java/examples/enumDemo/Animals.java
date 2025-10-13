package enumDemo;

public enum Animals {
    DOG("dog"),
    CAT("cat"),
    HORSE("horse"),

    private String aninalType;

    private Animals(String aninalType) {
        this.aninalType = aninalType;
    }

    public String getAnimalType() {
        return this.aninalType;
    }
}

