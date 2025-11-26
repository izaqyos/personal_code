class Solution:
    def repeat_str_util(self, repeat_count_str, new_len, chars):
        for j in range(len(repeat_count_str)):
            chars[new_len+j+1] = repeat_count_str[j] 

    def compress(self, chars: List[str]) -> int:
        if not chars:
            return 0
        if len(chars) == 1:
            return 1
        new_len = 0
        repeated_char = chars[0]
        first_repeated_index = 0
        for i,c in enumerate(chars):
            if c != repeated_char:
                if i-first_repeated_index == 1:
                    chars[new_len] = repeated_char
                    new_len+=1
                else:
                    chars[new_len] = repeated_char
                    repeat_count_str = str(i-first_repeated_index)
                    self.repeat_str_util(repeat_count_str, new_len, chars)
                    new_len+=1 + len(repeat_count_str)
                repeated_char = c
                first_repeated_index = i
        #print(f"new_len={new_len}, repeated_char={repeated_char}, first_repeated_index={first_repeated_index}")
        if repeated_char == chars[-1]:
            if len(chars)-first_repeated_index == 1:
               chars[new_len] = repeated_char
               new_len+=1
            else:
               chars[new_len] = repeated_char
               repeat_count_str = str(len(chars)-first_repeated_index)
               self.repeat_str_util(repeat_count_str, new_len, chars)
               new_len+=1 + len(repeat_count_str)

        return new_len
            
