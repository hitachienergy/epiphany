# Custom CA certificate/bundle

Note that for the comments below the filenames of the certificate(s)/bundle do not matter, only the extensions. The certificate(s)/bundle need to be placed here before building the devcontainer.

1. If you have one CA certificate you can add it here with the ```crt``` extension.
2. If you have multiple certificates in a chain/bundle you need to add them here individually with the ```crt``` extension and also add the single bundle with the ```pem``` extension containing the same certificates. This is needed unfortunally because not all tools inside the container except the single bundle.
