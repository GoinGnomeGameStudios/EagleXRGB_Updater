import hashlib
import json
import os

def create_update_metadata(package_path, version, min_required_version, base_url):
    # Calculate the SHA-256 hash of the package
    sha256_hash = hashlib.sha256()
    with open(package_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    package_hash = sha256_hash.hexdigest()

    # Get the package filename
    package_name = os.path.basename(package_path)

    # Create metadata
    metadata = {
        "latest_version": version,
        "package_name": package_name,
        "package_url": f"{base_url}/{package_name}",
        "package_hash": package_hash,
        "signature_file": f"{package_name}.sig",
        "signature_url": f"{base_url}/{package_name}.sig",
        "release_notes": f"{base_url}/release-notes-{version}.html",
        "min_required_version": min_required_version
    }

    # Write metadata to a file
    metadata_file = "update_metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"Update metadata created: {metadata_file}")
    print(f"Package hash: {package_hash}")

# Usage
base_url = "https://goingnomegamestudios.github.io/EagleXRGB_Updater"
create_update_metadata(
    package_path="EagleXRGB_update_package_8.3.4.zip",
    version="8.3.4",
    min_required_version="8.3.3",
    base_url=base_url
)