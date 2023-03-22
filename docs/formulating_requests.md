To be able to make a request, you need to decide on a few main points:

- Which variables do you want?
    - And in which dataset are these variables located? (E.g. ERA5-Land).
- For which years do you want the variable?
- Do you want to the data globally, or specify a bounding box (using `--area`).
- (*For pressure level data:*) on which levels do you want the data.

!!! note
    All available arguments are listed in the [CLI Reference](reference/arguments.md)


### Example request

A typical request in `era5cli` can look like the following:

```
era5cli hourly \
    --land \
    --variables 2m_temperature 2m_dewpoint_temperature \
    --startyear 2000 \
    --endyear 2020 \
    --splitmonths True \
    --area 53.6 3.3 50.7 7.5
```

This request asks for *hourly* data of the ERA5-*Land* dataset, more specifically the *2m_temperature* and *2m_dewpoint_temperature* variables.

Additionally, data from the year *2000* up to (and including) *2020* is requested, with the final files being *split up by months*.
Lastly, an *area* is extracted from the dataset (in this case only the Netherlands).

### Using the info command

To be able to formulate a request, you can make use of the `--help` and `info`
arguments in era5cli.

The `info` argument takes a name, out of the ones shown below. For example,

```
era5cli info levels
```
will list all available pressure levels.

| `info` argument | shows: |
|-----------------|-------|
| `levels` | available pressure levels |
| `2Dvars` | available single level / 2D variables |
| `3Dvars` | available pressure level / 3D variables |
| `land` | available variables in ERA5-land |

???+ tip
    You can enter a variable name (such as `total_precipitation`) to show if the variable is available, and in which list.

    For example:
    ```sh
    era5cli info total_precipitation
    ```

    returns:
    ```
    total_precipitation is in the list(s): 2Dvars, land
    ```

You can view the available variable names in the [CLI Reference](reference/variables.md)
