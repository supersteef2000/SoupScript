import java.util.Scanner;

public class PrimeCheck {
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        System.out.print("Enter a number: ");
        long number = input.nextLong();
        if(number < 2){
            System.out.println(number + " is not prime.");
            System.exit(0);
        }
        for(int i = 2; i <= java.lang.Math.sqrt(number); i++){
            long mod = number % i;
            if(mod == 0){
                System.out.println(number + " is not prime.");
                System.exit(0);
            }
        }
        System.out.println(number + " is prime.");
    }
}