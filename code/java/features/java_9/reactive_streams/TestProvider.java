public class TestProvider {
    public static void main(string[] args) {
        whenSubscribeToIt_thenShouldConsumeAll();

    }

    private static void whenSubscribeToIt_thenShouldConsumeAll()
            throws InterruptedException {

        // given
        SubmissionPublisher<String> publisher = new SubmissionPublisher<>();
        EndSubscriber<String> subscriber = new EndSubscriber<>();
        publisher.subscribe(subscriber);
        List<String> items = List.of("1", "x", "2", "x", "3", "x");

        // when
        assertThat(publisher.getNumberOfSubscribers()).isEqualTo(1);
        items.forEach(publisher::submit);
        publisher.close();

        // then
        await().atMost(1000, TimeUnit.MILLISECONDS)
                .until(
                        () -> assertThat(subscriber.consumedElements)
                                .containsExactlyElementsOf(items));
    }
}