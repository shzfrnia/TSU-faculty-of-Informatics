class StringGenerator():
    @staticmethod
    def make_unique_string(banned_strings, original_string, counter=2):
        """This method ganerate uniq string using counter.
        Note:
            This method is recursive.
        Args:
            banned_names: It is the array of banned strings.
            name: It is name which you would want.
            counter: You can set start value self. Default value begins with 2..n
        Returns:
            The different string with banned_strings.
        Examples:
            banned_strings = ['a','b','c']
            string = 'a'

            >>> print(make_unique_string(arr, string))
            a2
        """
        original_string_is_uniq = original_string not in banned_strings
        if original_string_is_uniq:
            return original_string
        else:
            new_string = original_string + str(counter)
            new_string_is_uniq = new_string not in banned_strings
            return new_string if new_string_is_uniq else StringGenerator.make_unique_string(banned_strings, original_string, counter + 1)
