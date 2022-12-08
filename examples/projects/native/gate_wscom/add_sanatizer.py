Import("env")
env.Append(CCFLAGS=["-fsanitize=thread"], LINKFLAGS=["-fsanitize=thread"])
