/*
 * Author: Pearl Romeo
 * Student Number: 87756082
 * Lab Section: L2L
 * Date: 2017 01 15
 * Purpose: Prompts the user for his/her name and prints
 * a welcome message on the screen.
 */

#include <stdio.h>
#include <stdlib.h>

#define _CRT_SECURE_NO_WARNINGS

/* Constants */
#define MAX_NAME_LENGTH 100

int main(void) {
    char name[MAX_NAME_LENGTH];

    printf("Please enter your first name: ");
    scanf("%s", name)
    printf("\nHello, %s, welcome to APSC 160!\n\n", name);

    system("PAUSE");
    return 0;
}