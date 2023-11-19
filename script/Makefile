CC=gcc
CFLAGS=-fPIC -shared -Wall -Wextra
TARGET1=script/snapshot/snapshot.so
SOURCE1=script/snapshot/snapshot.c
TARGET2=script/codeCoverage/ptraceDebugger.so
SOURCE2=script/codeCoverage/ptraceDebugger.c
all: $(TARGET1) $(TARGET2)

$(TARGET1): $(SOURCE1)
	$(CC) $(CFLAGS) -o $(TARGET1) $(SOURCE1)

$(TARGET2): $(SOURCE2)
	$(CC) $(CFLAGS) -o $(TARGET2) $(SOURCE2)


clean:
	rm -f $(TARGET1) $(TARGET2)
	