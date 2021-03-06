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

  FILE* fbranches = fopen(".beargit/.branches", "w");
  fprintf(fbranches, "%s\n", "master");
  fclose(fbranches);
   
  write_string_to_file(".beargit/.prev", "0000000000000000000000000000000000000000");
  write_string_to_file(".beargit/.current_branch", "master");

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

void next_commit_id_hw1(char* commit_id) {
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

int beargit_commit_hw1(const char* msg) {
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

// ---------------------------------------
// HOMEWORK 2 
// ---------------------------------------

// This adds a check to beargit_commit that ensures we are on the HEAD of a branch.
int beargit_commit(const char* msg) {
  char current_branch[BRANCHNAME_SIZE];
  read_string_from_file(".beargit/.current_branch", current_branch, BRANCHNAME_SIZE);

  if (strlen(current_branch) == 0) {
    fprintf(stderr, "ERROR: Need to be on HEAD of a branch to commit\n");
    return 1;
  }

  return beargit_commit_hw1(msg);
}

const char* digits = "61c";

void next_commit_id(char* commit_id) {
  char current_branch[BRANCHNAME_SIZE];
  read_string_from_file(".beargit/.current_branch", current_branch, BRANCHNAME_SIZE);

  // The first COMMIT_ID_BRANCH_BYTES=10 characters of the commit ID will
  // be used to encode the current branch number. This is necessary to avoid
  // duplicate IDs in different branches, as they can have the same pre-
  // decessor (so next_commit_id has to depend on something else).
  int n = get_branch_number(current_branch);
  for (int i = 0; i < COMMIT_ID_BRANCH_BYTES; i++) {
    // This translates the branch number into base 3 and substitutes 0 for
    // 6, 1 for 1 and c for 2.
    commit_id[i] = digits[n%3];
    n /= 3;
  }

  // Use next_commit_id to fill in the rest of the commit ID.
  next_commit_id_hw1(commit_id + COMMIT_ID_BRANCH_BYTES);
}


// This helper function returns the branch number for a specific branch, or
// returns -1 if the branch does not exist.
int get_branch_number(const char* branch_name) {
  FILE* fbranches = fopen(".beargit/.branches", "r");

  int branch_index = -1;
  int counter = 0;
  char line[FILENAME_SIZE];
  while(fgets(line, sizeof(line), fbranches)) {
    strtok(line, "\n");
    if (strcmp(line, branch_name) == 0) {
      branch_index = counter;
    }
    counter++;
  }

  fclose(fbranches);

  return branch_index;
}

/* beargit branch
 *
 * See "Step 6" in the homework 1 spec.
 *
 */

int beargit_branch() {
  /* COMPLETE THE REST */
  FILE* fbranches = fopen(".beargit/.branches", "r");
  char line[BRANCHNAME_SIZE], str[BRANCHNAME_SIZE];
  read_string_from_file(".beargit/.current_branch", str, BRANCHNAME_SIZE);
  while(fgets(line, sizeof(line), fbranches)) {
    strtok(line, "\n");
    if (strcmp(line, str) == 0){
      fprintf(stdout, "* %s\n", line);
    }
    else{
      fprintf(stdout, "  %s\n", line);
    }
  }
  fclose(fbranches);
  return 0;
}

/* beargit checkout
 *
 * See "Step 7" in the homework 1 spec.
 *
 */

int checkout_commit(const char* commit_id) {
  /* COMPLETE THE REST */
  char line[FILENAME_SIZE];
  FILE* findex = fopen(".beargit/.index", "r");
  while (fgets(line, sizeof(line), findex)){
    strtok(line, "\n");
    fs_rm(line);
  }
  fclose(findex);
  char str[COMMIT_ID_SIZE + 50], dir[COMMIT_ID_SIZE + 50];
  if (commit_id[0] != '0'){
    strcpy(str, ".beargit/");
    strcat(str, commit_id);
    strcpy(dir, str);
    strcat(str, "/.index");
    fs_cp(str, ".beargit/.index");
    findex = fopen(".beargit/.index", "r");
    while (fgets(line, sizeof(line), findex)){
      strtok(line, "\n");
      strcat(dir, "/");
      strcat(dir, line);
      strcpy(str, line);
      fs_cp(dir, str);
    }
    fclose(findex);
  }
  else{
    write_string_to_file(".beargit/.index", "");
  }
  write_string_to_file(".beargit/.prev", commit_id);
  return 0;
}

int is_it_a_commit_id(const char* commit_id) {
  /* COMPLETE THE REST */
  int i;
  if (strlen(commit_id) == 40){
    for (i = 0; i < 40; i++){
      if (commit_id[i] != '6' && commit_id[i] != '1' && commit_id[i] != 'c'){
        return 0;
      }
    }
    return 1;
  }
  else{
    return 0;
  }
}

int beargit_checkout(const char* arg, int new_branch) {
  // Get the current branch
  char current_branch[BRANCHNAME_SIZE];
  read_string_from_file(".beargit/.current_branch", current_branch, BRANCHNAME_SIZE);

  // If not detached, update the current branch by storing the current HEAD into that branch's file...
  // Even if we cancel later, this is still ok.
  if (strlen(current_branch)) {
    char current_branch_file[BRANCHNAME_SIZE+50];
    sprintf(current_branch_file, ".beargit/.branch_%s", current_branch);
    fs_cp(".beargit/.prev", current_branch_file);
  }

  // Check whether the argument is a commit ID. If yes, we just stay in detached mode
  // without actually having to change into any other branch.
  if (is_it_a_commit_id(arg)) {
    char commit_dir[FILENAME_SIZE] = ".beargit/";
    strcat(commit_dir, arg);
    if (!fs_check_dir_exists(commit_dir)) {
      fprintf(stderr, "ERROR: Commit %s does not exist\n", arg);
      return 1;
    }

    // Set the current branch to none (i.e., detached).
    write_string_to_file(".beargit/.current_branch", "");

    return checkout_commit(arg);
  }

  // Just a better name, since we now know the argument is a branch name.
  const char* branch_name = arg;

  // Read branches file (giving us the HEAD commit id for that branch).
  int branch_exists = (get_branch_number(branch_name) >= 0);

  // Check for errors.
  if (branch_exists && new_branch) {
    fprintf(stderr, "ERROR: A branch named %s already exists\n", branch_name);
    return 1;
  } else if (!branch_exists && !new_branch) {
    fprintf(stderr, "ERROR: No branch %s exists\n", branch_name);
    return 1;
  }

  // File for the branch we are changing into.
  char branch_file[BRANCHNAME_SIZE + 50] = ".beargit/.branch_";
  strcat(branch_file, branch_name);

  // Update the branch file if new branch is created (now it can't go wrong anymore)
  if (new_branch) {
    FILE* fbranches = fopen(".beargit/.branches", "a");
    fprintf(fbranches, "%s\n", branch_name);
    fs_cp(".beargit/.prev", branch_file); 
    fclose(fbranches);
  }

  write_string_to_file(".beargit/.current_branch", branch_name);

  // Read the head commit ID of this branch.
  char branch_head_commit_id[COMMIT_ID_SIZE];
  read_string_from_file(branch_file, branch_head_commit_id, COMMIT_ID_SIZE);

  // Check out the actual commit.
  return checkout_commit(branch_head_commit_id);
}
