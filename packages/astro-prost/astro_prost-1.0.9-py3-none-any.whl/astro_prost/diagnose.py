import astropy.units as u
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import SkyCoord

matplotlib.use("Agg")  # Use the Agg backend for non-GUI rendering
import os

from astropy.io import fits
from astropy.table import Table
from astropy.visualization import make_lupton_rgb
from astropy.wcs import WCS


def getimages(ra, dec, size=240, filters="grizy", type="stack"):
    """Query ps1filenames.py service to get a list of images.

    :param ra: Right ascension of position, in degrees.
    :type ra: float
    :param dec: Declination of position, in degrees.
    :type dec: float
    :param size: The image size in pixels (0.25 arcsec/pixel)
    :type size: int
    :param filters: A string with the filters to include
    :type filters: str
    :return: The results of the search for relevant images.
    :rtype: Astropy Table
    """

    service = "https://ps1images.stsci.edu/cgi-bin/ps1filenames.py"
    url = ("{service}?ra={ra}&dec={dec}&size={size}&format=fits" "&filters={filters}&type={type}").format(
        **locals()
    )
    table = Table.read(url, format="ascii")
    return table


def geturl(ra, dec, size=240, output_size=None, filters="grizy", format="jpg", color=False, type="stack"):
    """Get the URL for images in the table.

    :param ra: Right ascension of position, in degrees.
    :type ra: float
    :param dec: Declination of position, in degrees.
    :type dec: float
    :param size: The extracted image size in pixels (0.25 arcsec/pixel)
    :type size: int
    :param output_size: output (display) image size in pixels (default = size).
        The output_size has no effect for fits format images.
    :type output_size: int
    :param filters: The string with filters to include.
    :type filters: str
    :param format: The data format (options are \\"jpg\\", \\"png" or \\"fits\\").
    :type format: str
    :param color: If True, creates a color image (only for jpg or png format).
        If False, return a list of URLs for single-filter grayscale images.
    :type color: bool, optional
    :return: The url for the image to download.
    :rtype: str
    """

    if color and format == "fits":
        raise ValueError("color images are available only for jpg or png formats")
    if format not in ("jpg", "png", "fits"):
        raise ValueError("format must be one of jpg, png, fits")
    table = getimages(ra, dec, size=size, filters=filters, type=type)
    url = (
        "https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?" "ra={ra}&dec={dec}&size={size}&format={format}"
    ).format(**locals())
    if output_size:
        url = url + f"&output_size={output_size}"

    # sort filters from red to blue
    flist = ["yzirg".find(x) for x in table["filter"]]
    table = table[np.argsort(flist)]
    if color:
        if len(table) > 3:
            # pick 3 filters
            table = table[[0, len(table) // 2, len(table) - 1]]
        for i, param in enumerate(["red", "green", "blue"]):
            url = url + "&{}={}".format(param, table["filename"][i])
    else:
        urlbase = url + "&red="
        url = []
        for filename in table["filename"]:
            url.append(urlbase + filename)
    return url


def get_ps1_pic(path, objid, ra, dec, size, band, safe=False, save=False):
    """Downloads PS1 picture (in fits) centered at a given location.

    :param path: The filepath where the fits file will be saved.
    :type path: str
    :param objid: The PS1 objid of the object of interest (to save as filename).
    :type objid: int
    :param ra: Right ascension of position, in degrees.
    :type ra: float
    :param dec: Declination of position, in degrees.
    :type dec: float
    :param size: The extracted image size in pixels (0.25 arcsec/pixel)
    :type size: int
    :param band: The PS1 band.
    :type band: str
    :param safe: If True, include the objid of the object of interest in the filename
        (useful when saving multiple files at comparable positions).
    :type safe: bool, optional
    """

    fitsurl = geturl(ra, dec, size=size, filters=f"{band}", format="fits")
    fh = fits.open(fitsurl[0])
    if save:
        if safe:
            fh.writeto(path + f"/PS1_{objid}_{int(size*0.25)}arcsec_{band}.fits")
        else:
            fh.writeto(path + f"/PS1_ra={ra}_dec={dec}_{int(size*0.25)}arcsec_{band}.fits")
    else:
        return fh


def find_all(name, path):
    """Crawls through a directory and all its sub-directories looking for a file matching
       \\'name\\'. If found, it is returned.

    :param name: The filename for which to search.
    :type name: str
    :param path: The directory to search.
    :type path: str
    :return: The list of absolute paths to all files called \\'name\\' in \\'path\\'.
    :rtype: list
    """

    result = []
    for root, _, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def plot_match(
    host_ra,
    host_dec,
    true_host_ra,
    true_host_dec,
    host_z_mean,
    host_z_std,
    sn_ra,
    sn_dec,
    sn_name,
    sn_z,
    bayesflag,
    fn,
):
    """Short summary.

    Parameters
    ----------
    host_ra : type
        Description of parameter `host_ra`.
    host_dec : type
        Description of parameter `host_dec`.
    true_host_ra : type
        Description of parameter `true_host_ra`.
    true_host_dec : type
        Description of parameter `true_host_dec`.
    host_z_mean : type
        Description of parameter `host_z_mean`.
    host_z_std : type
        Description of parameter `host_z_std`.
    sn_ra : type
        Description of parameter `sn_ra`.
    sn_dec : type
        Description of parameter `sn_dec`.
    sn_name : type
        Description of parameter `sn_name`.
    sn_z : type
        Description of parameter `sn_z`.
    bayesflag : type
        Description of parameter `bayesflag`.
    fn : type
        Description of parameter `fn`.

    Returns
    -------
    type
        Description of returned object.

    """
    cols = np.array(
        [
            "#ff9f1c",
            "#2cda9d",
            "#f15946",
            "#da80dd",
            "#f4e76e",
            "#b87d4b",
            "#ff928b",
            "#c73e1d",
            "#58b09c",
            "#e7e08b",
        ]
    )
    bands = "zrg"
    if len(host_ra) > 0:
        sep = np.nanmax(
            SkyCoord(host_ra * u.deg, host_dec * u.deg)
            .separation(SkyCoord(sn_ra * u.deg, sn_dec * u.deg))
            .arcsec
        )
    else:
        sep = 0
    if true_host_ra:
        sep_true = (
            SkyCoord(true_host_ra * u.deg, true_host_dec * u.deg)
            .separation(SkyCoord(sn_ra * u.deg, sn_dec * u.deg))
            .arcsec
        )
        if (true_host_ra) and (true_host_dec) and (sep_true > sep):
            sep = sep_true
    rad = np.nanmax([30.0, 2 * sep])  # arcsec to pixels, scaled by 1.5x host-SN separation
    print(f"Getting img with size len {rad:.2f}...")
    pic_data = []
    for band in bands:
        get_ps1_pic("./", None, sn_ra, sn_dec, int(rad * 4), band)
        a = find_all(f"PS1_ra={sn_ra}_dec={sn_dec}_{int(rad)}arcsec_{band}.fits", ".")
        pixels = fits.open(a[0])[0].data
        pixels = pixels.astype("float32")
        # normalize to the range 0-255
        pixels *= 255 / np.nanmax(pixels)
        # plt.hist(pixels)
        pic_data.append(pixels)
        hdu = fits.open(a[0])[0]
        os.remove(a[0])

    lo_val, up_val = np.nanpercentile(
        np.array(pic_data).ravel(), (0.5, 99.5)
    )  # Get the value of lower and upper 0.5% of all pixels
    stretch_val = up_val - lo_val

    rgb_default = make_lupton_rgb(
        pic_data[0], pic_data[1], pic_data[2], minimum=lo_val, stretch=stretch_val, Q=0
    )
    wcs = WCS(hdu.header)
    plt.figure(num=None, figsize=(12, 8), facecolor="w", edgecolor="k")
    ax = plt.subplot(projection=wcs)
    ax.set_xlabel("RA", fontsize=24)
    ax.set_ylabel("DEC", fontsize=24)

    # really emphasize the supernova location
    plt.axvline(x=int(rad * 2), c="tab:red", alpha=0.5, lw=2)
    plt.axhline(y=int(rad * 2), c="tab:red", alpha=0.5, lw=2)

    if true_host_ra and true_host_dec:
        true_str = ""
        ax.scatter(
            true_host_ra,
            true_host_dec,
            transform=ax.get_transform("fk5"),
            marker="+",
            alpha=0.8,
            lw=2,
            s=200,
            color="magenta",
            zorder=100,
        )
    else:
        true_str = "(no true)"
    bayesstr = ". "
    if bayesflag == 2:
        bayesstr += "Strong match!"
        # don't plot the second-best host
        host_ra = host_ra[:1]
        host_dec = host_dec[:1]
    elif bayesflag == 1:
        bayesstr += "Weak match."
    if host_ra and host_dec:
        for i in np.arange(len(host_ra)):
            # print(f"Plotting host {i}")
            ax.scatter(
                host_ra[i],
                host_dec[i],
                transform=ax.get_transform("fk5"),
                marker="o",
                alpha=0.8,
                lw=2,
                s=100,
                edgecolor="k",
                facecolor=cols[i],
                zorder=100,
            )
        if sn_z == sn_z:
            plt.title(
                f"{sn_name}, z={sn_z:.4f}; Host Match,"
                f"z={host_z_mean:.4f}+/-{host_z_std:.4f} {true_str}{bayesstr}"
            )
        else:
            plt.title(
                f"{sn_name}, no z; Host Match, "
                f"z={host_z_mean:.4f}+/-{host_z_std:.4f} {true_str}{bayesstr}"
            )
    else:
        if sn_z == sn_z:
            plt.title(f"{sn_name}, z={sn_z:.4f}; No host found {true_str}")
        else:
            plt.title(f"{sn_name}, no z; No host found {true_str}")
    ax.imshow(rgb_default, origin="lower")
    plt.axis("off")
    plt.savefig("./%s.png" % fn, bbox_inches="tight")
    plt.close()


# Function to diagnose the discrepancy when the top-ranked galaxy is not the true host
def diagnose_ranking(
    true_index,
    post_probs,
    galaxy_catalog,
    post_offset,
    post_z,
    post_absmag,
    galaxy_ids,
    z_sn,
    sn_position,
    post_offset_true=None,
    post_z_true=None,
    post_absmag_true=None,
    verbose=False,
):
    """Short summary.

    Parameters
    ----------
    true_index : type
        Description of parameter `true_index`.
    post_probs : type
        Description of parameter `post_probs`.
    galaxy_catalog : type
        Description of parameter `galaxy_catalog`.
    post_offset : type
        Description of parameter `post_offset`.
    post_z : type
        Description of parameter `post_z`.
    post_absmag : type
        Description of parameter `post_absmag`.
    galaxy_ids : type
        Description of parameter `galaxy_ids`.
    z_sn : type
        Description of parameter `z_sn`.
    sn_position : type
        Description of parameter `sn_position`.
    post_offset_true : type
        Description of parameter `post_offset_true`.
    post_z_true : type
        Description of parameter `post_z_true`.
    post_absmag_true : type
        Description of parameter `post_absmag_true`.
    verbose : type
        Description of parameter `verbose`.

    Returns
    -------
    type
        Description of returned object.

    """
    top_indices = np.argsort(post_probs)[-3:][::-1]  # Top 3 ranked galaxies

    if verbose:
        if true_index > 0:
            print(f"True Galaxy: {true_index + 1}")

            # Check if the true galaxy is in the top 5
            if true_index not in top_indices:
                print(f"Warning: True Galaxy {true_index + 1} is not in the top 5!")

        # Print top 5 and compare with the true galaxy
        for rank, i in enumerate(top_indices, start=1):
            is_true = "(True Galaxy)" if i == true_index and true_index > 0 else ""
            print(
                f"Rank {rank}: ID {galaxy_ids[top_indices[rank-1]]}"
                f"has a Posterior probability of being the host: {post_probs[i]:.4f} {is_true}"
            )

    # Detailed comparison of the top-ranked and true galaxy
    print(f"Coords (SN): {sn_position.ra.deg:.4f}, {sn_position.dec.deg:.4f}")
    for _, i in enumerate(top_indices, start=1):
        top_gal = galaxy_catalog[i]
        top_theta = sn_position.separation(
            SkyCoord(ra=top_gal["ra"] * u.degree, dec=top_gal["dec"] * u.degree)
        ).arcsec

        if verbose:
            print(f"Redshift (SN): {z_sn:.4f}")
            print(f"Top Galaxy (Rank {i}): Coords: {top_gal['ra']:.4f}, {top_gal['dec']:.4f}")
            print(
                f"\t\t\tRedshift = {top_gal['z_best_mean']:.4f}+/-{top_gal['z_best_std']:.4f},"
                " Angular Size = {top_gal['angular_size_arcsec']:.4f} arcsec"
            )
            print(f"\t\t\tFractional Sep. = {top_theta/top_gal['angular_size_arcsec']:.4f} host radii")
            print(f'\t\t\tAngular Sep. ("): {top_theta:.2f}')
            print(f"\t\t\tRedshift Posterior = {post_z[i]:.4e}," " Offset Posterior = {post_offset[i]:.4e}")
            print(f"\t\t\tAbsolute mag Posterior = {post_absmag[i]:.4e}")

    if verbose and true_index > 0:
        true_gal = galaxy_catalog[true_index]
        true_theta = sn_position.separation(
            SkyCoord(ra=true_gal["ra"] * u.degree, dec=true_gal["dec"] * u.degree)
        ).arcsec
        print(f"True Galaxy: Fractional Sep. = {true_theta/true_gal['angular_size_arcsec']:.4f} host radii")
        print(
            f"\t\t\tRedshift = {true_gal['redshift']:.4f}, "
            f"Angular Size = {true_gal['angular_size_arcsec']:.4f}\""
        )
        print(f"\t\t\tRedshift Posterior = {post_z_true:.4e}, Offset Posterior = {post_offset_true:.4e}")

    if true_index > 0:
        post_offset_true = post_offset[true_index]

    if true_index > 0:
        post_z_true = post_z[true_index]

    ranked_indices = np.argsort(post_probs)[::-1]

    # Find the position of the true galaxy's index in the ranked list
    true_rank = np.where(ranked_indices == true_index)[0][0] if true_index > 0 else -1

    # Return the rank (0-based index) of the true galaxy
    return true_rank, post_probs[true_index]
