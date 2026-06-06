
export function getMenuItems(routes, routerPush, permissionCheckFn) {
    // 0. Load Folder Metadata
    const metaFiles = import.meta.glob('/src/pages/**/_meta.json', { eager: true });

    // Normalize meta: '/src/pages/Info/_meta.json' -> 'Info' (or 'Info/InfoDetail')
    const folderMeta = {};
    for (const path in metaFiles) {
        // remove /src/pages/ prefix and /_meta.json suffix
        const relative = path.replace('/src/pages/', '').replace('/_meta.json', '');
        folderMeta[relative] = metaFiles[path].default || metaFiles[path];
    }

    const items = [];

    // 1. Filter out ignored paths AND hidden routes
    const ignoredPaths = ['/login', '/', '/:all(.*)*'];
    const pageRoutes = routes.filter(r => {
        // Core ignores
        if (ignoredPaths.includes(r.path) || r.path.includes(':') || r.path.includes('*')) return false;

        // Meta: Hidden
        if (r.meta?.hidden) return false;

        // Meta: Permission Check
        if (permissionCheckFn && r.meta?.permission) {
            const hasAccess = permissionCheckFn(r.meta.permission);
            if (!hasAccess) return false;
        }

        return true;
    });

    // 2. Sort routes
    pageRoutes.sort((a, b) => a.path.localeCompare(b.path));

    pageRoutes.forEach(route => {
        const segments = route.path.split('/').filter(Boolean);
        let currentLevel = items;
        let currentPath = '';

        // FIX: Use for...of to allow breaking the loop when a folder is hidden.
        // forEach cannot be broken, which caused children to be added to the wrong level.
        for (const [index, segment] of segments.entries()) {
            currentPath = currentPath ? `${currentPath}/${segment}` : segment;

            // Check Folder Config (Pre-check for Hidden) - Case Insensitive Lookup
            const metaKey = Object.keys(folderMeta).find(k => k.toLowerCase() === currentPath.toLowerCase());
            const meta = metaKey ? folderMeta[metaKey] : null;

            if (meta?.hidden) {
                // IMPORTANT: Break strictly stops hidden folders AND their children
                break;
            }

            const isLast = index === segments.length - 1;
            const fullPath = route.path;

            // Default auto-formatting
            let label = segment
                .replace(/[-_]/g, ' ')
                .replace(/\b\w/g, c => c.toUpperCase());

            let icon = null;

            // Apply Folder Config (Title/Icon)
            if (meta) {
                if (meta.title) label = meta.title;
                if (meta.icon) icon = meta.icon;
            }

            // Route Meta Override (Leaf) - Winning over Folder Config
            if (isLast && route.meta) {
                if (route.meta.title) label = route.meta.title;
                if (route.meta.icon) icon = route.meta.icon;
            }

            let item = currentLevel.find(i => i.label === label);

            if (!item) {
                // Default Icon Fallback
                if (!icon) {
                    icon = isLast ? 'pi pi-file' : 'pi pi-folder';
                }

                item = {
                    label: label,
                    icon: icon,
                };

                if (isLast) {
                    item.command = () => routerPush(fullPath);
                    item.path = fullPath;
                } else {
                    item.items = [];
                }

                currentLevel.push(item);
            } else {
                // Folder exists. 
                if (!isLast && !item.items) {
                    item.items = [];
                    // Ensure Folder Icon is consistent with Config even if auto-generated first
                    if (meta && meta.icon) item.icon = meta.icon;
                    else item.icon = 'pi pi-folder';

                    delete item.command;
                }
            }

            // Descend
            if (item.items) {
                currentLevel = item.items;
            }
        }
    });

    // 3. Recursive Pruning of Empty Folders
    function pruneItems(items) {
        return items.filter(item => {
            if (item.items) {
                // Recurse
                item.items = pruneItems(item.items);

                // If folder is now empty, remove it (unless it also has a command, allowing clickable folders?)
                if (item.items.length === 0 && !item.command) {
                    return false;
                }
            }
            return true;
        });
    }

    return pruneItems(items);
}
