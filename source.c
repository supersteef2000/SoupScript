#include <stdio.h>
int main(void){
int number;
int root;
int loop;
int i;
int notprime;
int mod;
printf("Enter a number: ");
if (0 == scanf_s("%i", &number)) {
number = 0;
scanf_s("%*s");
}
root = 1;
loop = 1;
i = 0;
while (loop==1) {
i = i+1;
root = number/root+root;
root = root/2;
if (i==number+1) {
loop = 0;
}
}
if (number<2) {
printf("%i", (int)(number));
printf(" is not prime.\n");
notprime = 1;
}
i = 2;
while (i<=root) {
mod = number%i;
if (mod==0) {
printf("%i", (int)(number));
printf(" is not prime.\n");
notprime = 1;
i = root+1;
}
i = i+1;
}
if (notprime!=1) {
printf("%i", (int)(number));
printf(" is prime.\n");
}
return 0;
}
