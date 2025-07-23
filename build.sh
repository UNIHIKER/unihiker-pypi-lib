echo "clean..."
cd unihiker/
rm -rf dist/
rm -rf src/unihiker.egg-info

echo "build..."
#pip install --upgrade build
python -m build
echo "build done"