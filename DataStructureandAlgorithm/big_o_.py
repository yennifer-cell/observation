
import time

def up_to_n(n):
    
    
    sum=0
    for i in range(1,n+1):
        #print("I is ", "Sum is",sum)
        sum=sum+i
        
    print(f"when is n is {n} sum is {sum}")   
    return sum

def up_to_n_2(n):
    sum= n*(n+1)/2
    print(f"when is n is {n} sum is {sum}")
    return sum
    

    """
    op1+op2+op3+n*op4+op6
    remain=k
    k+k+k+n*k+k ==>
    --> 4k+n*k
    ---> simplify the operations
    --> 4k+n*k--> [4k , n*k]
    -->k=1 second --> [4,n]
    n=1--> [4,1]
    n=1000-->[4+1000]
    bigo is n(1)

    """

start_time=time.perf_counter()
up_to_n_2(1000)

end_time=time.perf_counter()

diff_ms=(end_time-start_time)*1000

print(f"\n Execution time:${diff_ms} ms ")


start_time=time.perf_counter()
up_to_n(1000)

end_time=time.perf_counter()

diff_ms=(end_time-start_time)*1000

print(f"\n Execution time:${diff_ms} ms ")