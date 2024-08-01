from langfuse.decorators import observe, langfuse_context
 
## 监听任意的函数的输入输出！！！

@observe()
def main(a):
    print("Hello, from the main function!")
    return(f"=========xxxxxxxxxx==={a}=====")
 
main("aaaaaa")
 
langfuse_context.flush()

# {
# args: [
# 0: "aaaaaa"
# ]
# kwargs: {
# }
# }
# Output
# 
# "=========xxxxxxxxxx===aaaaaa====="
# Metadata
# 
# null

