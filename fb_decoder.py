import flatbuffers
import ClientApp.Person
import ClientApp.Group
import ClientApp.Root
import ClientApp.Client
from ClientApp import Gender

def decode_person(person):
    print("Person:")
    print(f"  Name: {person.Name().decode('utf-8')}")
    print(f"  Age: {person.Age()}")
    print(f"  Weight: {person.Weight()}")
    gender = "Male" if person.Gender() == Gender.Gender.Male else "Female"
    print(f"  Gender: {gender}")

def decode_group(group):
    print("Group:")
    print(f"  Group Name: {group.GroupName().decode('utf-8')}")
    print(f"  Average Age: {group.AverageAge()}")
    print(f"  Average Weight: {group.AverageWeight()}")
    names = [group.Names(i).decode('utf-8') for i in range(group.NamesLength())]
    print(f"  Names: {', '.join(names)}")

def decode_client(root):
    client_type = root.ClientType()
    if client_type == ClientApp.Client.Client().Person:
        person = ClientApp.Person.Person()
        person.Init(root.Client().Bytes, root.Client().Pos)
        decode_person(person)
    elif client_type == ClientApp.Client.Client().Group:
        group = ClientApp.Group.Group()
        group.Init(root.Client().Bytes, root.Client().Pos)
        decode_group(group)
    else:
        print("Unknown client type")

def main():
    with open('fb_bytes.bin', 'rb') as f:
        data = f.read()

    offset = 0
    while offset < len(data):
        # Read the size prefix
        size = flatbuffers.encode.Get(flatbuffers.packer.uoffset, data, offset)
        offset += 4  # Move past the size prefix

        # Get the root object at the current offset
        root = ClientApp.Root.Root.GetRootAsRoot(data, offset)
        
        # Decode the current client
        decode_client(root)
        
        # Move to the next object in the buffer
        offset += size

if __name__ == "__main__":
    main()

