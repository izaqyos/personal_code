


import java.util.stream.IntStream;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
/**
 * @author yosi izaq
 * get kth permutation of n!
 * has to be fast so don't calculate perms (o(n!))
 *    n! is actually {1,2,...,n}! (all different permutations)
 *    A way to generate would be.
 *    1,{2,...,n}! 
 *    and
 *    2,{1,3,...n}!
 *    ...
 *    and
 *    n,(1,...,n-1}!
 *    note that given k we can know first digit. say we have list above indexed 0 (  1,{2,...,n}! ) to n-1 ( n,(1,...,n-1}!)
 *    we take k-1 and divide by (n-1)! , result index of first #. 
 *    Then we do (k-1)%((n-1)!) we get k1 (next index) repeat until n==1
 *
 */
class Solution {
        //private static final boolean bDebug = false;
        private static final boolean bDebug = true;
    public String getPermutation(int n, int k) {
            
            if (Solution.bDebug) System.out.printf("getPermutation(%d,%d)%n",n,k);
            String sRet = "";
            if (n <=0)
            {
                return "";
            }
            
            if (n==1)
            {
                if (k==1)
                {
                    return "1";
                }
                else
                {
                    return "";
                }
            }
            int [] perms = new int[n-1] ;
            int curr = 1;
            for (int i : IntStream.rangeClosed(1,n-1).toArray() )
            {
                    curr *= i;
                    perms[i-1] = curr;
            }
           
            if (Solution.bDebug) System.out.print("cache permutations= ");
            if (Solution.bDebug) System.out.println( Arrays.toString(perms));
            List<Integer> nums = IntStream.rangeClosed(1,n).boxed().collect(Collectors.toList());
            if (Solution.bDebug) System.out.print("nums list: ");
            if (Solution.bDebug) System.out.println( nums.stream().map(Object::toString).collect(Collectors.joining(",")));
            int index = k-1;
            int ithK = 0;
            for (int i=0; i<n-1;i++) //get n-1 digits of desired permutation. the last digit is the last remaining in nums list
            {
                    if (Solution.bDebug) System.out.printf("nums=[%s], i=%d, k=%d, permutation[%d]=%d %n",( nums.stream().map(Object::toString).collect(Collectors.joining(","))), i,index, n-i-2, perms[n-i-2]);
                    ithK = index/perms[n-i-2] ; //perms[j] has value (j+1)!. so this equals at 1st iteration k-1/(n-1)!
                    sRet+=Integer.toString(nums.get(ithK));
                    index = index%perms[n-i-2] ; 
                    nums.remove(ithK);
            }
            sRet +=Integer.toString(nums.get(0));
            return sRet;
        
    }
}

public class PermSeq
{
        public static void main (String[] args)
        {
                System.out.println("Test PermSeq.java");
                
                int[] permutations = IntStream.rangeClosed(0,9).toArray();
                System.out.print("permutations=[");
                for (int perm : permutations)
                {
                    System.out.print(perm+",");
                }
                System.out.println("]");
                int[] kthperm = {0,1,1,2,3,1,5,4,7,362880};
                Solution sol = new Solution();
                for (int i=0; i < permutations.length; i++)
                {
                        System.out.printf( "Solving get kth perm. n=%d, k=%d, ", permutations[i], kthperm[i]);
                        System.out.printf("Solution= %s%n%n", sol.getPermutation( permutations[i], kthperm[i] ));
                }
                return;
        }
}
