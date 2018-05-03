
class Assembly:
    """
    The assembly class holds all of the information regarding the assembly that is currently being built.

    args:
         assembly_data (DataFrame): information regarding the assembly in question
    """

    def __init__(self, assembly_data, assembly_type):
        """
        Initializes the Assembly class with its corresponding data and assembly type

        args:
           assembly_data (DataFrame): data frame which holds all of the information regarding the assembly
        return:
            void
        """
        self.assembly_data = assembly_data
        self.assembly_type = assembly_type


