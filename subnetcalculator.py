import re
import ipaddress

def is_valid_ip(ip):
    """Validate the IP address format."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

def is_valid_cidr(cidr):
    """Validate the CIDR format."""
    try:
        return 0 <= int(cidr) <= 32
    except ValueError:
        return False

def calculate_subnet_mask(cidr):
    """Calculate subnet mask from CIDR."""
    return str(ipaddress.IPv4Network((0, cidr)).netmask)

def get_network_class(ip):
    """Infer the class of the IP address and return default CIDR."""
    first_octet = int(ip.split('.')[0])
    if first_octet < 128:
        return 8  # Class A
    elif first_octet < 192:
        return 16  # Class B
    else:
        return 24  # Class C
def calculate_subnets(ip, cidr, partition_type, number):
    """Calculate subnet details based on the partition type and number."""
    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    if partition_type == "hosts":
        new_prefix = 32 - int(number).bit_length()
        subnets = list(network.subnets(new_prefix=new_prefix))
    else:  # subnets
        subnets = list(network.subnets(prefixlen_diff=int(number)))
    
    return {
        "Subnet Mask": str(network.netmask),
        "CIDR": f"/{network.prefixlen}",
        "Number of Hosts": network.num_addresses - 2,  # Excluding network and broadcast addresses
        "Number of Subnets": len(subnets),
        "First Two Subnets": subnets[:2],
        "Last Two Subnets": subnets[-2:]
    }
def main():
    ip = input("Enter an IP address: ")
    if not is_valid_ip(ip):
        print("Invalid IP address.")
        return
    
    cidr_input = input("Enter a CIDR (optional): ")
    cidr = int(cidr_input) if cidr_input and is_valid_cidr(cidr_input) else get_network_class(ip)
    
    partition_type = input("Partition by number of hosts or subnets? (hosts/subnets): ")
    if partition_type not in ["hosts", "subnets"]:
        print("Invalid partition type.")
        return
    
    number_input = input(f"Enter number of {partition_type}: ")
    if not number_input.isdigit():
        print("Invalid number.")
        return
    
    subnet_info = calculate_subnets(ip, cidr, partition_type, number_input)
    print(subnet_info)  # Display the calculated subnet information in a nicer format in the real implementation

if __name__ == "__main__":
    main()

