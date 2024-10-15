def f1():
    code = '''#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

void main() {
    char b[100];

    int fd = open("file1.txt", O_RDONLY);
    int fd1 = open("file3.txt", O_WRONLY | O_APPEND);

    int n = read(fd, b, 100);

    write(fd1, b, n);

    close(fd);
    close(fd1);
}
'''
    print(code)


def f2():
    code='''
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

void main() {
    char b[100];
    int fd = open("file1.txt", O_RDONLY);
    int fd1 = open("files.txt", O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    int n = read(fd, b, 100);
    write(fd1, b, n);
    close(fd);
    close(fd1);
}
'''
    print(code)



def f3():
    code='''#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

void main() {
    char b[1000];
    int fd = open("v1.txt", O_RDONLY);
    int fd1 = open("v2.txt", O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    int n = read(fd, b, 1000);
    write(fd1, b, n);
    close(fd);
    close(fd1);
}
'''
    print(code)


def f4():
    code='''
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

void main() {
    char b[200];
    int fd = open("file3.txt", O_RDWR);
    
    lseek(fd, -11, SEEK_END);
    int n = read(fd, b, 11);
    write(1, b, n);
    
    close(fd);
}
'''
    print(code)


def f5():
    code='''
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

void main() {
    char b[1000];
    int fd = open("v1.txt", O_RDONLY);
    
    int file_size = lseek(fd, 0, SEEK_END);
    int half = file_size / 2;
    
    lseek(fd, half, SEEK_SET);
    
    int n = read(fd, b, 1000);
    write(1, b, n);
    
    close(fd);
}

'''
    print(code)


def f6():
    code='''
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

void main() {
    char b[11];
    int fd = open("v1.txt", O_RDONLY);
    
    lseek(fd, 9, SEEK_SET);
    
    int n = read(fd, b, 10);
    write(1, b, n);
    
    close(fd);
}
'''
    print(code)


def fcfs():
    code='''
def findWaitingTime(processes, n, bt, at, wt, ct):
    wt[0] = 0
    ct[0] = at[0] + bt[0]
    
    for i in range(1, n):
        ct[i] = max(ct[i-1], at[i]) + bt[i]
        wt[i] = ct[i] - at[i] - bt[i]
        if wt[i] < 0:
            wt[i] = 0

def findTurnAroundTime(processes, n, bt, wt, tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]

def findavgTime(processes, n, bt, at):
    wt = [0] * n
    tat = [0] * n
    ct = [0] * n
    total_wt = 0
    total_tat = 0
    
    findWaitingTime(processes, n, bt, at, wt, ct)
    findTurnAroundTime(processes, n, bt, wt, tat)
    
    print("\nProcesses  Arrival time  Burst time  Waiting time  Turn around time  Completion Time")
    for i in range(n):
        total_wt += wt[i]
        total_tat += tat[i]
        print(f" {processes[i]}\t\t{at[i]}\t\t{bt[i]}\t\t{wt[i]}\t\t{tat[i]}\t\t{ct[i]}")
    
    print(f"\nAverage waiting time = {total_wt / n:.2f}")
    print(f"Average turn around time = {total_tat / n:.2f}")
    
    return wt, tat, ct

def printGanttChart(processes, bt, at, ct):
    print("\nGantt Chart:")
    n = len(processes)
    
    # Print process names
    for i in range(n):
        print(f"|  P{processes[i]}  ", end="")
    print("|")
    
    # Print timeline
    current_time = at[0]
    print(f"{current_time}", end="")
    for i in range(n):
        for _ in range(7):
            print(" ", end="")
        print(f"{ct[i]}", end="")
    print()

if __name__ == "__main__":
    n = int(input("Enter the number of processes: "))
    processes = list(range(1, n+1))
    burst_time = []
    arrival_time = []
    
    for i in range(n):
        at = int(input(f"Enter arrival time for process {i+1}: "))
        bt = int(input(f"Enter burst time for process {i+1}: "))
        arrival_time.append(at)
        burst_time.append(bt)
    
    # Sort processes based on arrival time
    processes = [x for _, x in sorted(zip(arrival_time, processes))]
    burst_time = [x for _, x in sorted(zip(arrival_time, burst_time))]
    arrival_time.sort()
    
    wt, tat, ct = findavgTime(processes, n, burst_time, arrival_time)
    printGanttChart(processes, burst_time, arrival_time, ct)'''
    print(code)

def sjf():
    code='''def main():
    n = int(input("Enter the number of processes: "))
    A = [[0 for j in range(5)] for i in range(n)]
    total_wt, total_tat = 0, 0

    arrival_times = list(map(int, input("Enter the arrival times of the processes (space-separated): ").split()))

    print("Enter the burst times of the processes:")
    for i in range(n):
        A[i][1] = int(input(f"Burst time for P{i + 1}: "))
        A[i][0] = i + 1
        A[i][4] = arrival_times[i]

    A.sort(key=lambda x: x[4])  # Sort by arrival time

    current_time = 0
    completed = 0
    gantt_chart = []
    is_completed = [False] * n

    while completed != n:
        idx = -1
        min_burst = float('inf')

        for i in range(n):
            if A[i][4] <= current_time and not is_completed[i]:
                if A[i][1] < min_burst:
                    min_burst = A[i][1]
                    idx = i

                if A[i][1] == min_burst:
                    if A[i][4] < A[idx][4]:
                        idx = i

        if idx != -1:
            start_time = current_time
            A[idx][2] = current_time - A[idx][4]  # Waiting Time
            A[idx][3] = A[idx][2] + A[idx][1]  # Turnaround Time
            current_time += A[idx][1]
            end_time = current_time
            is_completed[idx] = True
            completed += 1
            gantt_chart.append(f"P{A[idx][0]} [{start_time}-{end_time}]")

            total_wt += A[idx][2]
            total_tat += A[idx][3]
        else:
            current_time += 1  # If no process is ready, increment the current time

    avg_wt = total_wt / n
    avg_tat = total_tat / n

    print("P	 BT	 WT	 TAT	 AT")
    for i in range(n):
        print(f"P{A[i][0]}	 {A[i][1]}	 {A[i][2]}	 {A[i][3]}	 {A[i][4]}")

    print(f"Average Waiting Time= {avg_wt}")
    print(f"Average Turnaround Time= {avg_tat}")
    print("Gantt Chart: " + " -> ".join(gantt_chart))


if __name__ == "__main__":
    main()
'''
    print(code)

def rr():
    code = '''def find_waiting_time(processes, n, bt, wt, at, quantum):
    rem_bt = bt.copy()
    t = 0
    gantt = []
    completion_time = [0] * n
    queue = []
    completed = 0
    
    while completed != n:
        for i in range(n):
            if at[i] <= t and rem_bt[i] > 0 and i not in queue:
                queue.append(i)
        
        if not queue:
            t += 1
            gantt.append(("Idle", 1))
            continue
        
        i = queue.pop(0)
        if rem_bt[i] > quantum:
            t += quantum
            rem_bt[i] -= quantum
            gantt.append((processes[i], quantum))
            for j in range(n):
                if at[j] <= t and rem_bt[j] > 0 and j not in queue and j != i:
                    queue.append(j)
            queue.append(i)
        else:
            t += rem_bt[i]
            gantt.append((processes[i], rem_bt[i]))
            completion_time[i] = t
            wt[i] = t - at[i] - bt[i]
            rem_bt[i] = 0
            completed += 1
    
    return gantt, completion_time

def find_turnaround_time(processes, n, bt, wt, tat, ct, at):
    for i in range(n):
        tat[i] = ct[i] - at[i]

def find_avg_time(processes, n, bt, quantum, at):
    wt = [0] * n
    tat = [0] * n
    
    gantt, completion_time = find_waiting_time(processes, n, bt, wt, at, quantum)
    find_turnaround_time(processes, n, bt, wt, tat, completion_time, at)
    
    print("\nProcesses    Arrival Time    Burst Time    Waiting Time    Turn-Around Time    Completion Time")
    total_wt = total_tat = 0
    for i in range(n):
        total_wt += wt[i]
        total_tat += tat[i]
        print(f" {processes[i]:<12} {at[i]:<15} {bt[i]:<13} {wt[i]:<15} {tat[i]:<19} {completion_time[i]}")
    
    print(f"\nAverage waiting time = {total_wt/n:.5f}")
    print(f"Average turn around time = {total_tat/n:.5f}")
    
    print("\nGantt Chart:")
    print("-" * 80)
    for process, duration in gantt:
        print(f"|{process:^{duration*2}}", end="")
    print("|")
    print("-" * 80)
    
    current_time = 0
    for _, duration in gantt:
        print(f"{current_time:<{duration*2}}", end="")
        current_time += duration
    print(current_time)

if __name__ == "__main__":
    n = int(input("Enter the number of processes: "))
    processes = []
    burst_time = []
    arrival_time = []
    
    for i in range(n):
        processes.append(input(f"Enter name for process {i+1}: "))
        arrival_time.append(int(input(f"Enter arrival time for process {processes[-1]}: ")))
        burst_time.append(int(input(f"Enter burst time for process {processes[-1]}: ")))
    
    quantum = int(input("Enter time quantum: "))
    
    find_avg_time(processes, n, burst_time, quantum, arrival_time)'''
    print(code)


def fork():
    code='''
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    int a = 2;
    pid_t pid;
    pid = fork();

    printf("%d\n", pid);

    if (pid < 0) {
        printf("FORK FAILED\n");
    } else if (pid == 0) {
        printf("CHILD PROCESS \t a is: ");
        printf("%d\n", ++a);
    } else {
        printf("PARENT PROCESS \t a is: ");
        printf("%d\n", --a);
    }

    printf("EXITING WITH X = %d\n", a);
    
    return 0;
}
'''
    print(code)


def orphan():
    code='''
#include <stdio.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {  // Error in creating a child
        printf("Child cannot be created\n");
    } 
    else if (pid > 0) {  // Parent section
        printf("Process id of child = %d\n", pid);
        printf("Process id of parent = %d\n", getpid());
    } 
    else {  // Child section
        sleep(1);  // Simulate delay to show the child becoming an orphan
        printf("Process id of child = %d\n", getpid());
        printf("Process id of parent = %d\n", getppid());  // Shows parent's process ID
    }

    return 0;
}
'''
    print(code)


def sleep():
    code='''
#include <stdio.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {  // Error in creating a child
        printf("Child cannot be created\n");
    } 
    else if (pid > 0) {  // Parent section
        sleep(1);  // Sleep to ensure child doesn't become orphan
        printf("Process id of child = %d\n", pid);  // pid holds child's PID
        printf("Process id of parent = %d\n", getpid());
    } 
    else {  // Child section
        printf("Process id of child = %d\n", getpid());
        printf("Process id of parent = %d\n", getppid());
    }

    return 0;
}
'''
    print(code)


def shared1():
    code='''
// Writer process (P1)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>

int main() {
    // Generate a unique key
    key_t key = ftok("shmfile", 65);

    // Get the shared memory ID
    int shmid = shmget(key, 1024, 0666 | IPC_CREAT);

    // Attach to the shared memory
    char *str = (char*) shmat(shmid, (void*)0, 0);

    // Write data to shared memory
    printf("Write Data: ");
    fgets(str, 1024, stdin);  // User input

    printf("Data written in memory: %s\n", str);

    // Detach from the shared memory
    shmdt(str);

    return 0;
}
'''
    print(code)


def shared2():
    code='''
// Reader process (P2)
#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>

int main() {
    // Generate a unique key
    key_t key = ftok("shmfile", 65);

    // Get the shared memory ID
    int shmid = shmget(key, 1024, 0666);

    // Attach to the shared memory
    char *str = (char*) shmat(shmid, (void*)0, 0);

    // Read data from shared memory
    printf("Data read from memory: %s\n", str);

    // Detach from the shared memory
    shmdt(str);

    // Destroy the shared memory after reading
    shmctl(shmid, IPC_RMID, NULL);

    return 0;
}
'''
    print(code)


def pipe():
    code='''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main() {
    int pipefds[2];
    pid_t pid;
    char write_msg[100];
    char read_msg[100];

    // Create a pipe
    if (pipe(pipefds) == -1) {
        perror("Pipe failed");
        return 1;
    }

    // Fork a child process
    pid = fork();

    if (pid < 0) {
        perror("Fork failed");
        return 1;
    }

    if (pid > 0) {
        // Parent process - Writer
        close(pipefds[0]); // Close the read end of the pipe

        printf("Parent (P1): Enter a message: ");
        fgets(write_msg, sizeof(write_msg), stdin);

        // Write to the pipe
        write(pipefds[1], write_msg, strlen(write_msg) + 1);
        close(pipefds[1]); // Close the write end after writing

        // Wait for child process to finish
        wait(NULL);
    } else {
        // Child process - Reader
        close(pipefds[1]); // Close the write end of the pipe

        // Read from the pipe
        read(pipefds[0], read_msg, sizeof(read_msg));
        printf("Child (P2): Received message: %s\n", read_msg);

        close(pipefds[0]); // Close the read end after reading
    }

    return 0;
}'''
    print(code)

def client():
    code='''
import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 8080)
client_socket.connect(server_address)
print("Connected to server...")

try:
    while True:
        # Input message to send to the server
        message = input("Client (type 'exit' to close connection): ")
        client_socket.sendall(message.encode())
        
        # Check if the client wants to close the connection
        if message.lower() == 'exit':
            print("Client has closed the connection.")
            break

        # Receive the response from the server
        data = client_socket.recv(1024).decode()
        if data.lower() == 'exit':
            print("Server has closed the connection.")
            break
        print(f"Server: {data}")

finally:
    # Clean up the connection
    client_socket.close()
    print("Connection closed.")
'''
    print(code)

def server():
    code='''
import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 8080)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening on port 8080...")

# Wait for a connection
connection, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

try:
    while True:
        # Receive the data from the client
        data = connection.recv(1024).decode()
        if data.lower() == 'exit':
            print("Client has closed the connection.")
            break
        print(f"Client: {data}")
        
        # Input message to send to the client
        response = input("Server (type 'exit' to close connection): ")
        connection.sendall(response.encode())
        
        # Check if the server wants to close the connection
        if response.lower() == 'exit':
            print("Server has closed the connection.")
            break

finally:
    # Clean up the connection
    connection.close()
    server_socket.close()
    print("Connection closed.")
'''
    print(code)
