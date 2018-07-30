#include <stdio.h>
#include <string.h>

#include <unistd.h>
#include <sys/stat.h>

#include "beargit.h"
#include "util.h"

/* Implementation Notes:
 *
 * - Functions return 0 if successful, 1 if there is an error.
 * - All error conditions in the function description need to be implemented
 *   and written to stderr. We catch some additional errors for you in main.c.
 * - Output to stdout needs to be exactly as specified in the function description.
 * - Only edit this file (beargit.c)
 * - You are given the following helper functions:
 *   * fs_mkdir(dirname): create directory <dirname>
 *   * fs_rm(filename): delete file <filename>
 *   * fs_mv(src,dst): move file <src> to <dst>, overwriting <dst> if it exists
 *   * fs_cp(src,dst): copy file <src> to <dst>, overwriting <dst> if it exists
 *   * write_string_to_file(filename,str): write <str> to filename (overwriting contents)
 *   * read_string_from_file(filename,str,size): read a string of at most <size> (incl.
 *     NULL character) from file <filename> and store it into <str>. Note that <str>
 *     needs to be large enough to hold that string.
 *  - You NEED to test your code. The autograder we provide does not contain the
 *    full set of tests that we will run on your code. See "Step 5" in the homework spec.
 */

/* beargit init
 *
 * - Create .beargit directory
 * - Create empty .beargit/.index file
 * - Create .beargit/.prev file containing 0..0 commit id
 *
 * Output (to stdout):
 * - None if successful
 */

int beargit_init(void) {
  fs_mkdir(".beargit");

  FILE* findex = fopen(".beargit/.index", "w");
  fclose(findex);
  
  write_string_to_file(".beargit/.prev", "0000000000000000000000000000000000000000");

  return 0;
}


/* beargit add <filename>
 * 
 * - Append filename to list in .beargit/.index if it isn't in there yet
 *
 * Possible errors (to stderr):
 * >> ERROR: File <filename> already added
 *
 * Output (to stdout):
 * - None if successful
 */

int beargit_add(const char* filename) {
  FILE* findex = fopen(".beargit/.index", "r");
  FILE *fnewindex = fopen(".beargit/.newindex", "w");

  char line[FILENAME_SIZE];
  while(fgets(line, sizeof(line), findex)) {
    strtok(line, "\n");
    if (strcmp(line, filename) == 0) {
      fprintf(stderr, "ERROR: File %s already added\n", filename);
      fclose(findex);
      fclose(fnewindex);
      fs_rm(".beargit/.newindex");
      return 3;
    }

    fprintf(fnewindex, "%s\n", line);
  }

  fprintf(fnewindex, "%s\n", filename);
  fclose(findex);
  fclose(fnewindex);

  fs_mv(".beargit/.newindex", ".beargit/.index");

  return 0;
}


/* beargit rm <filename>
 * 
 * See "Step 2" in the homework 1 spec.
 *
 */

int beargit_rm(const char* filename) {
  /* COMPLETE THE REST */
  FILE* findex = fopen(".beargit/.index", "r");
  FILE* fnewindex = fopen(".beargit/.newindex", "w");
  char line[FILENAME_SIZE], str[FILENAME_SIZE + 100];
  int flag = 0;
  while(fgets(line, sizeof(line), findex)) {
    strtok(line, "\n");
    if (strcmp(line, filename) != 0) {
      fprintf(fnewindex, "%s\n", line);
    }
    else{
      flag = 1;
    }
  }
  fclose(findex);
  fclose(fnewindex);
  if (flag == 1){
    fs_mv(".beargit/.newindex", ".beargit/.index");
    return 0;
  }
  else{
    strcpy(str, "ERROR: File ");
    strcat(str, filename);
    strcat(str, " not tracked");
    fprintf(stderr, "%s\n", str);
    return 1;
  }
}

/* beargit commit -m <msg>
 *
 * See "Step 3" in the homework 1 spec.
 *
 */

const char* go_bears = "GO BEARS!";

int is_commit_msg_ok(const char* msg) {
  /* COMPLETE THE REST */
  int i = 0, j = 0, k;
  while (msg[i] != '\0'){
    k = i;
    if (msg[i] == go_bears[j]){
      while (msg[i] == go_bears[j]){
        i++;
        j++;
        if (go_bears[j] == '\0'){
          return 1;
        }
        if (msg[i] == '\0'){
          return 0;
        }
      }
    }
    i = k + 1;
    j = 0;
  }
  return 0;
}

void next_commit_id(char* commit_id) {
  /* COMPLETE THE REST */
  int i, length;
  int a[COMMIT_ID_SIZE];
  length = strlen(commit_id);
  for (i = 0; i < length; i++){
    if (commit_id[i] == '6'){
      a[i] = 0;
    }
    else if (commit_id[i] == '1'){
      a[i] = 1;
    }
    else{
      a[i] = 2;
    }
  }
  i = length - 1;
  while (a[i] == 2){
    a[i] = 0;
    i--;
  }
  a[i]++;
  for (i = 0; i < length; i++){
    if (a[i] == 0){
      commit_id[i] = '6';
    }
    else if (a[i] == 1){
      commit_id[i] = '1';
    }
    else{
      commit_id[i] = 'c';
    }
  }
}

int beargit_commit(const char* msg) {
  if (!is_commit_msg_ok(msg)) {
    fprintf(stderr, "ERROR: Message must contain \"%s\"\n", go_bears);
    return 1;
  }

  int i;
  char commit_id[COMMIT_ID_SIZE], line[FILENAME_SIZE], dir[COMMIT_ID_SIZE + 50], str[FILENAME_SIZE + 100];
  read_string_from_file(".beargit/.prev", commit_id, COMMIT_ID_SIZE);
  if (commit_id[0] == '0'){
    for (i = 0; i < strlen(commit_id); i++){
      commit_id[i] = '6';
    }
  }
  else{
    next_commit_id(commit_id);
  }

  /* COMPLETE THE REST */
  FILE* findex = fopen(".beargit/.index", "r");
  strcpy(dir, ".beargit/"); 
  strcat(dir, commit_id);
  fs_mkdir(dir);
  strcpy(str, dir);
  strcat(str, "/.index");
  fs_cp(".beargit/.index", str);
  strcpy(str, dir);
  strcat(str, "/.prev");
  fs_cp(".beargit/.prev", str);
  while(fgets(line, sizeof(line), findex)){
    strtok(line, "\n");
    strcpy(str, dir);
    strcat(str, "/");
    strcat(str, line);
    fs_cp(line, str);
  }
  strcat(dir, "/.msg");
  write_string_to_file(dir, msg);
  write_string_to_file(".beargit/.prev", commit_id);
  fclose(findex);
  return 0;
}

/* beargit status
 *
 * See "Step 1" in the homework 1 spec.
 *
 */

int beargit_status() {
  /* COMPLETE THE REST */
  FILE* findex = fopen(".beargit/.index", "r");
  char line[FILENAME_SIZE];
  int s = 0;
  fprintf(stdout, "%s\n", "Tracked files:");
  fprintf(stdout, "%s\n", "");
  while(fgets(line, sizeof(line), findex)) {
    strtok(line, "\n");
    fprintf(stdout, "  %s\n", line);
    s++;
  }
  fprintf(stdout, "%s\n", "");
  fprintf(stdout, "%d %s\n", s, "files total");
  fclose(findex);
  return 0;
}

/* beargit log
 *
 * See "Step 4" in the homework 1 spec.
 *
 */

int beargit_log() {
  /* COMPLETE THE REST */
  char commit_id[COMMIT_ID_SIZE], msg[MSG_SIZE], dir[COMMIT_ID_SIZE + 100], str[COMMIT_ID_SIZE + 100];
  read_string_from_file(".beargit/.prev", commit_id, COMMIT_ID_SIZE);
  if (commit_id[0] == '0'){
    fprintf(stderr, "%s\n", "ERROR: There are no commits!");
    return 1;
  }
  else{
    fprintf(stdout, "%s\n", "");
    while (commit_id[0] != '0'){
      strcpy(str, "commit ");
      strcat(str, commit_id);
      fprintf(stdout, "%s\n", str);
      strcpy(dir, ".beargit/");
      strcat(dir, commit_id);
      strcat(dir, "/.msg");
      read_string_from_file(dir, msg, MSG_SIZE);
      strcpy(str, "    ");
      strcat(str, msg);
      fprintf(stdout, "%s\n", str);
      fprintf(stdout, "%s\n", "");
      strcpy(dir, ".beargit/");
      strcat(dir, commit_id);
      strcat(dir, "/.prev");
      read_string_from_file(dir, commit_id, COMMIT_ID_SIZE);
    }
    return 0;
  }
}
