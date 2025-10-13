class ProcessHandleDemo {
    public static void main(String[] args) {
        ProcessHandle.allProcesses().forEach(process -> {
            String user = process.info().user().orElse("N/A");
            if (user.equals("i500695")) { //print my processes 
                System.out.printf("PID=%d, Command=%s, Arguments=%s, Start time=%s, user=%s \n", process.pid(),
                        process.info().command().orElse("N/A"),
                        String.join(" ", process.info().arguments().orElse(new String[] {})),
                        process.info().startInstant().orElse(null),
                        process.info().user().orElse("N/A"));

            }
        });

    }
}