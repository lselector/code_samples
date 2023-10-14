#! /bin/env python2.7

"""
# test_file_speed.py
# multiple tests or writing/reading files
# using different uncompressed and compressed formats
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

import subprocess, errno
import StringIO as sio
import io, tarfile, zipfile, zlib, gzip

import myutil
reload(myutil)
from myutil import *

import myutil_dt
reload(myutil_dt)
from myutil_dt import *

# ---------------------------------------------------------------
@timing
def make_sure_dir_exists(bag, mydir):
    """
    # tries to (re)create a directory
    # if directory already exists - does nothing
    # if directory doesn't exist, but we can't create it,
    # will fail with error
    """
    print_func_name(bag)
    try:
        os.makedirs(mydir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            print "Can not create directory ", mydir
            raise

# ---------------------------------------------------------------
@timing
def create_df_float(bag):
    """
    # creates bag.df_float with bag.nrows rows.
    # columns are of type float64
    """
    print_func_name(bag)
    print "creating DataFrame with %s rows" % commify(bag.nrows)
    ncols = 12
    # ---------------------------------- 
    # create float columns fc001, fc002, ...
    colnames = ["fc%03d" % x for x in range(ncols)]
    df = pd.DataFrame(np.random.randn(bag.nrows,ncols), 
                      index=range(bag.nrows), columns=colnames)

    bag.df_float = df

# ---------------------------------------------------------------
@timing
def create_df_num(bag):
    """
    # creates bag.df_num with bag.nrows rows.
    # columns are of two types: float64 & int64
    """
    print_func_name(bag)
    print "creating DataFrame with %s rows" % commify(bag.nrows)
    ncols = 6
    # ---------------------------------- 
    # create float columns fc001, fc002, ...
    colnames = ["fc%03d" % x for x in range(ncols)]
    df = pd.DataFrame(np.random.randn(bag.nrows,ncols), 
                      index=range(bag.nrows), columns=colnames)
    # ---------------------------------- 
    # add integer columns ic001, ic002, ...
    for col in colnames:
        df['i'+col[1:]] = df[col].map(lambda x: int(1000*x) if x==x else 0)

    bag.df_num = df

# ---------------------------------------------------------------
@timing
def create_df(bag):
    """
    # creates bag.df with bag.nrows rows.
    # columns are of different types: float, integer, strings
    """
    print_func_name(bag)
    print "creating DataFrame with %s rows" % commify(bag.nrows)
    ncols = 4
    # ---------------------------------- 
    # create float columns fc001, fc002, ...
    colnames = ["fc%03d" % x for x in range(ncols)]
    df = pd.DataFrame(np.random.randn(bag.nrows,ncols), 
                      index=range(bag.nrows), columns=colnames)
    # ---------------------------------- 
    # add integer columns ic001, ic002, ...
    for col in colnames:
        df['i'+col[1:]] = df[col].map(lambda x: int(1000*x) if x==x else 0)
    # ---------------------------------- 
    # add character columns cc001, cc002, ...
    for col in colnames:
        df['c'+col[1:]] = df[col].map(lambda x: "c%09.6f"%x if x==x else 0)

    bag.df = df


# ---------------------------------------------------------------
def __gunzip(gziped_contents):
    """
    # gunzip provided contents uzing external zcat command.
    # zcat used to be faster than built-in gzip library,
    # but nowadays they are the same speed.
    """
    pp = subprocess.Popen(  ['zcat'], 
                            stdin  = subprocess.PIPE, 
                            stdout = subprocess.PIPE  )
    myout, myerr = pp.communicate(gziped_contents)

    return myout

# ---------------------------------------------------------------
@timing
def write_df_zip_1step(bag):
    """
    # writes a dataframe into a .zip file
    """
    print_func_name(bag)
    ss = bag.df.to_csv(None, sep='|', index=False, header=True)
    zz = zipfile.ZipFile(bag.fname_zip_full, mode='w', 
                         compression=zipfile.ZIP_DEFLATED)
    zz.writestr(zinfo_or_arcname=bag.fname, bytes=ss)

# ---------------------------------------------------------------
@timing
def write_df_zip_2step(bag):
    """
    # writes a dataframe into a .zip file
    # by first writing into an uncompressed file, and then zip-ing it
    """
    print_func_name(bag)
    mylog(bag, "writing file " + bag.fname_full)
    bag.df.to_csv(bag.fname_full, sep='|', index=False, header=True)
    mylist = [ "cd %s; zip %s %s" % (bag.subdir, bag.fname_zip, bag.fname), # create zip file
               "rm -f %s" % (bag.fname_full) ]                               # remove uncompressed
    for mycmd in mylist:
        run_cmd(bag, mycmd)

# ---------------------------------------------------------------
@timing
def read_df_zip(bag):
    """
    # reads compressed delimited file into dataframe
    # returns dataframe
    """
    print_func_name(bag)
    mylog(bag, "reading file " + bag.fname_zip_full)
    zz = zipfile.ZipFile(bag.fname_zip_full, 'r')    # zz = zip_object
    bag.zz = zz
    bag.df_zip = pd.read_csv(zz.open(bag.fname), sep='|')

# ---------------------------------------------------------------
@timing
def df_to_str(bag):
    """
    # populates bag.df_str - string representation of bag.df
    """
    print_func_name(bag)
    bag.df_str = bag.df.to_csv(None, sep='|', index=False, header=True)

# ---------------------------------------------------------------
@timing
def str_to_strio(bag):
    """
    # creates bag.df_strio 
    # as a StringIO wrapper around bag.df_str
    # (this is very fast operation)
    """
    print_func_name(bag)
    bag.df_strio = sio.StringIO(bag.df_str)

# ---------------------------------------------------------------
@timing
def str_to_list(bag):
    """
    # creates bag.str_list
    """
    print_func_name(bag)
    mylist = bag.df_str.split("\n")
    bag.str_list = [ss+"\n" for ss in mylist]

# ---------------------------------------------------------------
@timing
def write_df_tsv(bag):
    """
    # writes a dataframe into a TSV file
    """
    print_func_name(bag)
    bag.df.to_csv(bag.fname_full, sep='|', index=False, header=True)

# ---------------------------------------------------------------
@timing
def write_strio_tgz(bag):
    """
    # writes string bag.df_strio into tar.gz file
    """
    print_func_name(bag)
    tar = tarfile.open(bag.fname_targz, 'w:gz')
    info       = tar.tarinfo()
    info.name  = bag.fname
    info.uname = str(os.getuid())
    info.gname = str(os.getgid())
    info.size  = bag.df_strio.len
    # -----------------------
    tar.addfile(info, bag.df_strio)
    tar.close()

# ---------------------------------------------------------------
@timing
def write_df_tgz(bag):
    """
    # writes bag.df into tar.gz file
    # by first converting it to string, and then writing the string
    """
    print_func_name(bag)
    # -----------------------
    ss = bag.df.to_csv(None, sep='|', index=False, header=True)
    ss_io = sio.StringIO(ss)
    # -----------------------
    tar = tarfile.open(bag.fname_targz, 'w:gz')
    info       = tar.tarinfo()
    info.name  = bag.fname
    info.uname = str(os.getuid())
    info.gname = str(os.getgid())
    info.size  = ss_io.len
    # -----------------------
    tar.addfile(info, ss_io)
    tar.close()

# ---------------------------------------------------------------
@timing
def read_df_tgz(bag):
    """
    # read DF from tar.gz file
    """
    tar = tarfile.open(mode="r:gz", fileobj=file(bag.fname_targz))
    fh = tar.extractfile(bag.fname)
    bag.df_tgz = pd.read_csv(fh, sep='|')

# ---------------------------------------------------------------
@timing
def write_str_gz(bag):
    """
    # writes a string into gz file
    """
    print_func_name(bag)
    fh = gzip.open(bag.fname_gz, 'wb')
    fh.write(bag.df_str)
    fh.close()

# ---------------------------------------------------------------
@timing
def write_df_gz_chunks(bag):
    """
    # writes data into a gz file in chunks.
    # In real life the chunks may be formed like this:
    #   while (have more data):
    #       fill DF to approx 10K rows
    #       convert DF to CSV string, write as one chunk
    #       delete DF
    # Here we get chunks by slicing one DF, so we get
    # the same output file as in other tests.
    # Note: this method is slower than writing to
    #   an uncompressed file, and then gziping the whole file
    """
    print_func_name(bag)
    fh = gzip.open(bag.fname_tmp, 'wb', 4)
    len_chunk = 10000
    len_df = len(bag.df)
    mypos = 0
    while mypos < len_df:
        mypos2 = mypos+len_chunk
        if mypos2>len_df:
            mypos2 = len_df
        df_tmp = bag.df[mypos:mypos2]
        myheader = True if mypos==0 else False
        content = df_tmp.to_csv(None, sep='|', index=False, header=myheader)
        fh.write(content)
        mypos = mypos2
    fh.close()
    os.rename(bag.fname_tmp, bag.fname_gz)

# ---------------------------------------------------------------
@timing
def write_df_gz_1step(bag):
    """
    # writes a dataframe into a dat.gz file
    # by first writing into a string, and writing
    # string into gzip file.
    """
    print_func_name(bag)
    ss = bag.df.to_csv(None, sep='|', index=False, header=True) # , chunksize=10000)
    fh = gzip.open(bag.fname_gz, 'wb', compresslevel=4)
    fh.write(ss)
    fh.close()

# ---------------------------------------------------------------
@timing
def write_df_gz_1step_buffered(bag):
    """
    # writes a dataframe into a dat.gz file
    # by first writing into a string, and writing
    # string into gzip file.
    """
    print_func_name(bag)
    with gzip.open(bag.fname_gz, 'wb', compresslevel=4) as fh:
        with io.BufferedWriter(fh) as mybuf:
            bag.df.to_csv(mybuf, sep='|', index=False, header=True) # , chunksize=10000)

# ---------------------------------------------------------------
@timing
def write_df_gz_2step(bag):
    """
    # writes a dataframe into a dat.gz file
    # by first writing into an uncompressed file, and then gziping it
    """
    print_func_name(bag)
    bag.df.to_csv(bag.fname_full, sep='|', index=False, header=True) # , chunksize=10000)
    mycmd = "gzip -4 --force " + bag.fname_full
    run_cmd(bag, mycmd)

# ---------------------------------------------------------------
@timing
def read_df_gz1(bag):
    """
    # reads dataframe from a gz file
    """
    print_func_name(bag)
    fh = gzip.open(bag.fname_gz, 'r')
    bag.df_gz1 = pd.read_csv(fh, sep='|')

# ---------------------------------------------------------------
@timing
def read_df_gz2(bag):
    """
    # reads dataframe from a gz file
    """
    print_func_name(bag)
    bag.df_gz2 = pd.read_csv(bag.fname_gz, sep='|', compression='gzip')

# ---------------------------------------------------------------
@timing
def read_df_gz3(bag):
    """
    # reads dataframe from a gz file
    """
    print_func_name(bag)
    with open(bag.fname_gz, 'rb') as fh:
        txt = __gunzip(fh.read())
    bag.df_gz3 = pd.read_csv(sio.StringIO(txt), sep='|')

# ---------------------------------------------------------------
@timing
def read_gz1(bag):
    """
    # reads strings from a gz file
    # populates bag.str_list1
    """
    print_func_name(bag)
    with gzip.open(bag.fname_gz, 'rb') as fh:
        bag.str1 = fh.read()

# ---------------------------------------------------------------
@timing
def read_gz2(bag):
    """
    # reads gz file as a binary blob.
    # uncompresses it using external zcat command
    # populates bag.str_list2
    """
    print_func_name(bag)
    with open(bag.fname_gz, 'rb') as fh:
        bag.str2 = __gunzip(fh.read())

# ---------------------------------------------------------------
@timing
def write_list_chunks_gz(bag, mylist, fname, add_newlines=False,
                              comprlevel=4, chunk_len=10000):
    """ 
    # writes a list of strings to gzip file fname
    # To maximize speed, this does two things: 
    #  (a) uses compression level 4 as a good compromise between speed and file size,
    #  (b) writes in chunks 
    """
    print_func_name(bag)
    n_total = len(mylist)
    n1 = 0
    n2 = chunk_len
    fh = gzip.open(fname, 'wb', comprlevel)
    while n1 < n_total :
        chunk = mylist[n1:n2]
        if not len(chunk):
            break
        if add_newlines:
            ss = '\n'.join(chunk) + '\n'
        else:
            ss = ''.join(chunk)
        fh.write(ss)
        n1 = n2
        n2 += chunk_len
    fh.close()

# ---------------------------------------------------------------
def __write_df_hdf5(bag, fname=None, bkey='', func='', complevel=0, complib='blosc'):
    """
    # called from different h5 write tests
    """
    if os.path.isfile(fname):
        os.remove(fname)
    # debug_here()
    try:
        if complevel == 0:
            store = pd.HDFStore(fname)
        else:
            store = pd.HDFStore(fname, complevel=complevel, complib=complib)
        store['my_df'] = bag[bkey] # save to file
        store.close()
    except:
        bag.exclude[func] = 1
        print "Can't write into hdf5"

# ---------------------------------------------------------------
def __read_df_hdf5(bag, fname=None, bkey='', func=''):
    """
    # called from different h5 read tests
    """
    try:
        store = pd.HDFStore(fname)
        bag[bkey] = store['my_df']
        store.close()
    except:
        bag.exclude[func] = 1
        print "Can't read from hdf5"

# ---------------------------------------------------------------
@timing
def write_df_h5(bag, complevel=0, complib='blosc'):
    """
    # test writing into hdf5 format: float, int, char
    """
    print_func_name(bag)
    func_name = get_func_name()
    fname = bag.fname_h5
    if complib != 'blosc':
        fname = fname + "." + complib
    __write_df_hdf5(bag, fname=fname, bkey='df', func=func_name, 
                         complevel=complevel, complib=complib)

# ---------------------------------------------------------------
@timing
def read_df_h5(bag):
    """
    # test reading hdf5 format: float, int, char
    """
    print_func_name(bag)
    func_name = get_func_name()
    __read_df_hdf5(bag, fname=bag.fname_h5, bkey='df', func=func_name)

# ---------------------------------------------------------------
@timing
def write_df_h5_float(bag, complevel=0, complib='blosc'):
    """
    # test writing into hdf5 format: float
    """
    print_func_name(bag)
    func_name = get_func_name()
    fname = bag.fname_float_h5
    if complib != 'blosc':
        fname = fname + "." + complib
    __write_df_hdf5(bag, fname=fname, bkey='df_float', func=func_name, 
                         complevel=complevel, complib=complib)

# ---------------------------------------------------------------
@timing
def read_df_h5_float(bag):
    """
    # test reading hdf5 format: float
    """
    print_func_name(bag)
    func_name = get_func_name()
    __read_df_hdf5(bag, fname=bag.fname_float_h5, bkey='df_float', func=func_name)

# ---------------------------------------------------------------
@timing
def write_df_h5_num(bag, complevel=0, complib='blosc'):
    """
    # test writing into hdf5 format: float & int
    """
    print_func_name(bag)
    func_name = get_func_name()
    fname = bag.fname_num_h5
    if complib != 'blosc':
        fname = fname + "." + complib
    __write_df_hdf5(bag, fname=fname, bkey='df_num', func=func_name, 
                         complevel=complevel, complib=complib)

# ---------------------------------------------------------------
@timing
def read_df_h5_num(bag):
    """
    # test reading hdf5 format: float & int
    """
    print_func_name(bag)
    func_name = get_func_name()
    __read_df_hdf5(bag, fname=bag.fname_num_h5, bkey='df_num', func=func_name)

# ---------------------------------------------------------------
def write_df_cpickle(bag):
    """
    # procedure to write DF using pickle
    """
    print_func_name(bag)
    # pickle_write(bag, bag.df, bag.fname_pickle)
    for protocol in range(3):
        fname = "junk/test%d.pickle" % protocol
        label = "write_df_cpickle%d"%protocol
        print label
        t1 = time.time()
        pickle.dump(bag.df, open(fname, "wb"), protocol=protocol)
        timing_add(bag, label, time.time()-t1)

# ---------------------------------------------------------------
@timing
def read_df_cpickle(bag):
    """
    # read pickle file into DF
    """
    print_func_name(bag)
    bag.df_pickle = pickle_read(bag, bag.fname_pickle)

# ---------------------------------------------------------------
@timing
def write_df_luis_num(bag):
    """
    # save DataFrame or Series (data) to a file (fname)
    # adapted from Luis Pedro Coelho 
    # https://gist.github.com/luispedro/7887214
    """
    print_func_name(bag)
    fname = bag.fname_luis
    data  = bag.df_num
    np.save(open(fname, 'w'), data)          # dump DataFrame to file
    # ----------------------------------
    # add metadata (index, columns) to the same file
    meta_tuple = (data.index, data.columns)
    ss = pickle.dumps(meta_tuple)            
    ss = ss.encode('string_escape')
    fh = open(fname, 'a')
    fh.seek(0, 2)  # offset=0, 
                   # whence=2 means move relative to the end of the file
    fh.write(ss)
    fh.close() 

# ---------------------------------------------------------------
@timing
def read_df_luis_num(bag):
    """
    # Load DataFrame or Series (see also save_pandas(fname, data))
    # adapted from Luis Pedro Coelho 
    # https://gist.github.com/luispedro/7887214
    # mmap_mode - optional string, same as numpy.load option
    """
    print_func_name(bag)
    import numpy.lib
    fname = bag.fname_luis
    vals  = np.load(fname, mmap_mode='r')
    # ------------------------ read meta data (index, columns)
    fh = open(fname)
    numpy.lib.format.read_magic(fh)
    numpy.lib.format.read_array_header_1_0(fh)
    fh.seek(vals.dtype.alignment * vals.size, 1)
    meta_tuple = pickle.loads(fh.readline().decode('string_escape'))
    fh.close()
    # ------------------------ recreate the DataFrame
    bag.df_luis = pd.DataFrame(vals, index=meta_tuple[0], columns=meta_tuple[1])

# ---------------------------------------------------------------
def set_fnames(bag):
    """
    # sets bag.fname* strings
    """
    bag.fname          = "test.dat"
    bag.fname_full     = bag.subdir + "/" + "test.dat"
    bag.fname_zip      = "test.zip"
    bag.fname_zip_full = bag.subdir + "/" + "test.zip"
    bag.fname_gz       = bag.subdir + "/" + "test.dat.gz"
    bag.fname_targz    = bag.subdir + "/" + "test.tar.gz"
    bag.fname_tmp      = bag.subdir + "/" + "test.tmp"
    bag.fname_h5       = bag.subdir + "/" + "test.h5"
    bag.fname_float_h5 = bag.subdir + "/" + "test_float.h5"
    bag.fname_num_h5   = bag.subdir + "/" + "test_num.h5"
    bag.fname_pickle   = bag.subdir + "/" + "test.pickle"
    bag.fname_luis     = bag.subdir + "/" + "test.luis"
    bag.exclude = dict()
    make_sure_dir_exists(bag, bag.subdir)

# ---------------------------------------------------------------
def create_dataframes(bag):
    """
    # create bag.df, bag.df_float, bag.df_num    
    """
    create_df(bag)          # bag.df (float, int, char)
    create_df_float(bag)    # bag.df_float
    create_df_num(bag)      # bag.df_num (float & int)

# ---------------------------------------------------------------
def do_luis(bag):
    """
    # run tests using "luis" method of saving/reading DF
    """
    if not bag.run_luis:
        return
    write_df_luis_num(bag)
    read_df_luis_num(bag)

# ---------------------------------------------------------------
def change_last_timing_name(bag, myname):
    """
    # changes last element in the list bag.timing
    # It is a tuple (name, time)
    # substitutes name with myname
    """
    if len(bag.timing) <= 0:
        return
    n1, t1 = bag.timing[-1]
    bag.timing[-1] = (myname,t1)

# ---------------------------------------------------------------
def do_hdf5(bag):
    """
    # save/read using HDF5
    """
    if not bag.run_hdf5:
        return
    write_df_h5_float(bag, complevel=8, complib='blosc')
    change_last_timing_name(bag,'write_df_h5_float_comp8_blosc')
    write_df_h5_float(bag, complevel=8, complib='lzo')
    change_last_timing_name(bag,'write_df_h5_float_comp8_lzo')
    read_df_h5_float(bag)
    # -----------------------
    write_df_h5_num(bag, complevel=8, complib='blosc')
    change_last_timing_name(bag,'write_df_h5_num_comp8_blosc')
    write_df_h5_num(bag, complevel=8, complib='lzo')
    change_last_timing_name(bag,'write_df_h5_num_comp8_lzo')
    read_df_h5_num(bag)
    # -----------------------
    write_df_h5(bag, complevel=8, complib='blosc')
    change_last_timing_name(bag,'write_df_h5_comp8_blosc')
    write_df_h5(bag, complevel=8, complib='lzo')
    change_last_timing_name(bag,'write_df_h5_comp8_lzo')
    read_df_h5(bag)

# ---------------------------------------------------------------
def do_df_gz(bag):
    """
    # write/read dataframe to/from gzip file
    """
    if not bag.run_df_gz:
        return
    write_df_gz_1step(bag)
    write_df_gz_1step_buffered(bag)
    write_df_gz_2step(bag)
    write_df_gz_chunks(bag)
    read_df_gz1(bag)
    read_df_gz2(bag)
    read_df_gz3(bag)
    read_gz1(bag)                   # into bag.str_list1
    read_gz2(bag)                   # into bag.str_list2

# ---------------------------------------------------------------
def do_df_zip(bag):
    """
    # write/read dataframe to/from zip file
    """
    if not bag.run_df_zip:
        return
    write_df_zip_1step(bag)
    write_df_zip_2step(bag)
    read_df_zip(bag)

# ---------------------------------------------------------------
def do_other(bag):
    """
    # does some other tests (not the fastest ones)
    """
    if not bag.run_other:
        return
    df_to_str(bag)          # bag.df_str
    str_to_strio(bag)       # bag.df_strio
    str_to_list(bag)        # bag.str_list
    write_df_tsv(bag)       # uncompressed
    write_strio_tgz(bag)
    write_df_tgz(bag)
    read_df_tgz(bag)
    write_str_gz(bag)
    write_list_chunks_gz(bag, bag.str_list, bag.fname_gz)

# ---------------------------------------------------------------
def do_pickle(bag):
    """
    # tries pickle
    """
    if not bag.run_pickle:
        return
    write_df_cpickle(bag)
    read_df_cpickle(bag)

# ---------------------------------------------------------------
@timing
def write_several_gz_into_zip(bag):
    """
    # create a zip file containing several gzip files
    """
    print_func_name(bag)
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ---------------------------------------------------------------
@timing
def read_several_gz_from_zip(bag, pos=0):
    """
    # Reads a gzip file from a zip file.
    # The zip file contains mane (~100) gzip files.
    # We want to test if time to extract the first one (pos=0)
    # is less than the time to extract the last one (pos=-1)
    """
    print_func_name(bag)
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ---------------------------------------------------------------
def do_random(bag):
    """
    # Procedure to test random access time withing a big compressed file.
    # According to Dan, extracting files form tar.gz is slow,
    # because TAR (Tape Archive) only provides sequential access,
    # so in order to reach the last file, the reader will read 
    # through all other files first. 
    # zip file is better because it has some sort of Table of Contents / Index.
    """
    if not bag.run_random:
        return
    write_several_gz_into_zip(bag)
    read_several_gz_from_zip(bag,0)
    read_several_gz_from_zip(bag,-1)

#    write_several_gz_into_targz(bag)
#    read_several_gz_from_targz(bag,0)
#    read_several_gz_from_targz(bag,-1)

# ---------------------------------------------------------------
def main(bag):
    """
    # main
    """
    myinit(bag)
    bag.mask_log_str = ""
    print_start_time(bag)
    bag.subdir     = "junk"
    set_fnames(bag)
    # ----------------------------------
    # select data size and which tests to run
    bag.nrows      = int(1e6)
    bag.run_luis   = False
    bag.run_hdf5   = False
    bag.run_df_gz  = True
    bag.run_df_zip = False
    bag.run_other  = False
    bag.run_pickle = True
    bag.run_random = False     # speed of randon access
    # ----------------------------------
    create_dataframes(bag)
    do_luis(bag)
    do_hdf5(bag)
    do_df_gz(bag)
    do_df_zip(bag)
    do_other(bag)
    do_pickle(bag)
    do_random(bag)  # reading files from zip with many files
    # ----------------------------------
    print "\nResults for %d rows:" % bag.nrows
    print "path =", bag.subdir
    print_timing(bag, exclude=bag.exclude)
    print_elapsed_time(bag)

# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)
