#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

void win()
{
    char flag[256];
    int flag_fd;
    int flag_length;

    flag_fd = open("/flag", 0);
    if (flag_fd < 0)
    {
        printf("\n  ERROR: Failed to open the flag -- %s!\n", strerror(errno));
        if (geteuid() != 0)
        {
            printf("  Your effective user id is not 0!\n");
            printf("  You must directly run the suid binary in order to have the correct permissions!\n");
        }
        exit(-1);
    }
    flag_length = read(flag_fd, flag, sizeof(flag));
    if (flag_length <= 0)
    {
        printf("\n  ERROR: Failed to read the flag -- %s!\n", strerror(errno));
        exit(-1);
    }
    write(1, flag, flag_length);
    printf("\n\n");
}

int main() {

  FILE *fptr;
  int seed;

  fptr = fopen("/challenge/super_secret_seed", "r");

  if(fptr == NULL) {
    printf("Error reading file\n");
    exit(1);
  }

  if(fscanf(fptr, "%d", &seed) != 1) {
    printf("Error reading seed from file.\n");
  }

  // printf("Seed: %d\n", seed);

  srandom(seed);

  printf("Now we're about to print the first three random values using this seed:\n\n");

  for(int i=0; i<3; i++) {
    int x = random();
    printf("%d\n", x);
  }

  printf("Now you need to input the next five random values generated using this seed:\n\n");

  for(int i=0; i<5; i++) {
    int x = random();

    int input;

    printf("Input the next rand number in the series: ");
    fscanf(stdin, "%d", &input);
    printf("\n");

    if(input != x) {
      printf("Try again ya nooob!");
      exit(1);
    }
  }

  win();

  return 0;
}
