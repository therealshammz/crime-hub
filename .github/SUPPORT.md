# Support

## Getting Help

If you have questions or need help with this project, you can:

1. **Check the documentation** - Read the [README.md](README.md) and [COMMANDS.md](COMMANDS.md) files
2. **Open an issue** - If you've found a bug or have a feature request, open an issue on the [GitHub Issues page](https://github.com/therealshammz/crime-hub/issues)
3. **Check existing issues** - Someone may have already reported the same issue

## Common Issues

### Data Not Found

If you get a "File not found" error when running the pipeline:

1. Ensure you've downloaded the data: `python scripts/download_data.py`
2. Check that the file exists: `ls -la dataset/crimes.csv`
3. Verify HDFS is running: `hdfs dfs -ls /`

### Java Version Errors

If you get Java-related errors:

1. Ensure Java 11 is installed for Hadoop
2. Ensure Java 17 is installed for Spark
3. Set JAVA_HOME appropriately: `export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64`

### Output Directory Exists

If Hadoop/Spark jobs fail with "Output directory already exists":

```bash
make clean-all
```

## Contributing

If you'd like to contribute, please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.