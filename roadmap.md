## Branch to complete the intended pull request completed during the internship

- urlib to complete download of zip files, see answer 2 with ~190 here: https://stackoverflow.com/questions/9419162/download-returned-zip-file-from-url

- urlib with password manager: answer 2 with 17 votes: https://stackoverflow.com/questions/23576970/python-handling-username-and-password-for-url

- gridfile with urls of tiles and the and the actual filename of the tiles when downloaded: https://github.com/justinelliotmeyers/TanDEM-X_GRID_INDEX

- buildvrt python function in skysat_stereo

- gdaladdo and other functions have python api as well (see geolib)


### Roadmap:

- User will input bounding box coord, username, password, download directory and a flag to whether delete temporary files or not
- Compute interestst with the tandem-x grid files
- Download all the intersecting tandem-x tiles, unzip (parallel)
- perform correction using: https://github.com/dshean/tandemx/blob/master/tandemx_mask.py
- build overviews and vrts
- End job

