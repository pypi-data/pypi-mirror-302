
class VocoChat:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"

def main():
    example = VocoChat("World")
    print(example.greet())

if __name__ == "__main__":
    main()
