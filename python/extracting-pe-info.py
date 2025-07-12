import click
import pefile

@click.command()
@click.option('--file', help='Input executable file')
@click.option('--output', help='Output file name')
@click.option('--disable-ASLR', '-d', is_flag=True, help="Disable ASLR for this executable")
def run(file, output, disable_aslr):
    """Simple program prints Optional header information from a PE File and can disable ASLR."""
    pe = pefile.PE(file)

    print(f'Address of Entry Point: {hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}')
    print(f'Address of Image Base: {hex(pe.OPTIONAL_HEADER.ImageBase)}')
    print(f'ASLR Enabled? {pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE}')
    
    # disable ASLR and write to new file
    if disable_aslr:
        pe.OPTIONAL_HEADER.DllCharacteristics &= ~pefile.DLL_CHARACTERISTICS['IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE']
        pe.write(output)
        print(f'Disabled ASLR and wrote to new file: {output}')

if __name__ == '__main__':
    run()