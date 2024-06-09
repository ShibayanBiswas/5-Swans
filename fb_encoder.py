import flatbuffers
import ClientApp.Person
import ClientApp.Group
import ClientApp.Root
import ClientApp.Client
import ClientApp.Gender

def create_person(builder, name, age, weight, gender):
    name_offset = builder.CreateString(name)
    ClientApp.Person.PersonStart(builder)
    ClientApp.Person.PersonAddName(builder, name_offset)
    ClientApp.Person.PersonAddAge(builder, age)
    ClientApp.Person.PersonAddWeight(builder, weight)
    ClientApp.Person.PersonAddGender(builder, gender)
    return ClientApp.Person.PersonEnd(builder)

def create_group(builder, group_name, average_age, average_weight, names):
    group_name_offset = builder.CreateString(group_name)
    names_offsets = [builder.CreateString(name) for name in names]
    ClientApp.Group.GroupStartNamesVector(builder, len(names))
    for offset in reversed(names_offsets):
        builder.PrependUOffsetTRelative(offset)
    names_vector = builder.EndVector()
    ClientApp.Group.GroupStart(builder)
    ClientApp.Group.GroupAddGroupName(builder, group_name_offset)
    ClientApp.Group.GroupAddAverageAge(builder, average_age)
    ClientApp.Group.GroupAddAverageWeight(builder, average_weight)
    ClientApp.Group.GroupAddNames(builder, names_vector)
    return ClientApp.Group.GroupEnd(builder)

def main():
    builder = flatbuffers.Builder(0)

    # Create a person
    person = create_person(builder, "Ram", 21, 76.5, ClientApp.Gender.Gender.Male)
    ClientApp.Root.RootStart(builder)
    ClientApp.Root.RootAddClientType(builder, ClientApp.Client.Client.Person)
    ClientApp.Root.RootAddClient(builder, person)
    root = ClientApp.Root.RootEnd(builder)
    builder.FinishSizePrefixed(root)  # Use size-prefixed buffer

    with open('fb_bytes.bin', 'wb') as f:
        f.write(builder.Output())

    # Reset builder for the group
    builder = flatbuffers.Builder(0)

    # Create a group
    group = create_group(builder, "FightClub", 24.5, 66, ["Ram", "Shyam", "Raghuveer"])
    ClientApp.Root.RootStart(builder)
    ClientApp.Root.RootAddClientType(builder, ClientApp.Client.Client.Group)
    ClientApp.Root.RootAddClient(builder, group)
    root = ClientApp.Root.RootEnd(builder)
    builder.FinishSizePrefixed(root)  # Use size-prefixed buffer

    with open('fb_bytes.bin', 'ab') as f:
        f.write(builder.Output())

if __name__ == "__main__":
    main()

