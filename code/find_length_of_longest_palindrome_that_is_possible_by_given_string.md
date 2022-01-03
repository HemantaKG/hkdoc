## Find The Length of Longest Palindrome Number of Even Length of Given Number
### Name: find_palindrome_len_v1.c

```c
/*
*********************************************************************************************************
* Find The Length of Longest Palindrome Number of Even Length of Given Number
* Name: find_palindrome_len_v1.c
*
*Problem Statement
*INPUT:
*	The imput contains one argument. A string S consisting of digits(0-9). 
*	First and only line of input consists of S (1<= |S|<= 100000).
*OUTPUT:
*	You must return a single interger denoting the length of longest sub-array
*	whose elements (digits) can be rearranged to form a Palindrome of even length.
* If no such sub-array can be found return 0.
*********************************************************************************************************
*
* How run?
* ./fpl 12314534234235
*********************************************************************************************************
*
*SAMPLE Test
*Case01: INPUT: 12345354987 => OUTPUT: 6 (i.e 345354 can be rearranged to form a Palindrome string)
*Case02: INPUT: 12345 => OUTPUT: 0
*********************************************************************************************************
*
*Hemanta Kumar G
*20171220
*********************************************************************************************************
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int checkPalindrome(char *);
int removeCHAR(char *, char, char *);

int main(int a, char* str[]){
	char *s= str[1];
	int plen= 0;
	
	//1. find all possible sub strings	 
	//2. process only even length strings
	//3. even length Palindrome number => even number of unique elements. 
	
	int slen= strlen(s);
	
	//outer for-loop works like
	//outer for-loop generates a sub-string by removing one char from end of the input string on each itiration.
	//EX: 1234 => itiration1: 1234, itiration2: 123, itiration3: 12, itiration4: treminates
	
	//inner for-loop works like
	//inner for-loop generates a sub-string by removing one char from front of the string that it got from outter for-loop on each itiration
	//EX: 1234 (got from itiration1 outer for-loop) => itiration1: 1234, itiration2: 234, itiration3: 34, itiration4: terminates
	
	
	for(int i= slen; i >=2; i--){
		char * tmp1= (char *) malloc(i* sizeof(char));
		strncpy(tmp1, s, i);
		tmp1[i]= '\0';
		//printf("tmp1: %s\n", tmp1);
		
		for(int j= 0; j<= i-2; j++){
			char * tmp2= (char *) malloc(i* sizeof(char));
			//copy substring from position "j" of tmp1, into tmp2
			strcpy(tmp2, &tmp1[j]);
			//printf("tmp2: %s\n", tmp2);
			
			if(strlen(tmp2)%2== 0){
				//printf("string: %s\n", tmp2);
				int nplen= checkPalindrome(tmp2);
				if(plen < nplen){
					plen= nplen;
					//printf("string: %s\n", tmp2);
				}
			}
			free(tmp2);
		}
		free(tmp1);
	}
	printf("Palindrome len: %d\n", plen);
	return 0;
}

int checkPalindrome(char * tmp2){
	int count= 0;
	int flag=1, plen= 0;
	int tmp2_len= strlen(tmp2);
	
	//remove identical char for string "tmp2" and count the number of identical char removed. Place the new string into "tmp3" 
	//if char count is even then copy string form "tmp3" to "tmp2" and call funtion "removeCHAR()" 
	//untill string length get 0 or char count is odd then breake loop
	
	while(1){
		if (strlen(tmp2)== 0){
			break;
		}
		else{
			char * tmp3= (char*) malloc(strlen(tmp2)* sizeof(char));
			count= removeCHAR(tmp2, tmp2[0], tmp3);
			if(count%2 != 0){
				flag=0;
				free(tmp3);
				break;
			}else{
				strcpy(tmp2,tmp3);
			}
			free(tmp3);
		}
	}

	if(flag)
		plen= tmp2_len;
	
	return plen;
}

int removeCHAR(char * tmp2, char ch, char * tmp3){
	int count=0;
	char * tmp2_bck= tmp2;
	char * tmp3_add_bck= tmp3;
	 
	while(*tmp2 != '\0'){
		if(*tmp2 != ch){
			*tmp3= *tmp2;
			tmp3++;
			}
			tmp2++;
		}
		*(tmp3)='\0';
		tmp3= tmp3_add_bck;
		tmp2= tmp2_bck;
		//printf("---removeCHAR---tmp3:%s---len(tmp2):%ld---len(tmp3):%ld\n", tmp3, strlen(tmp2), strlen(tmp3));
	count= strlen(tmp2)- strlen(tmp3);
	return count;
}

```
